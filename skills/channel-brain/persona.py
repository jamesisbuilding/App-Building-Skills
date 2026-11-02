#!/usr/bin/env python3
"""
persona — turn a channel brain into spawnable people. Each persona's memory IS its
wiki brain; you later spawn it in-character to talk to it.

  build:  python3 persona.py build <brain-dir> [--who synthesis|auto|host|guests|"Name1,Name2"]
                                               [--jobs 5] [--min N]
  list:   python3 persona.py list

Default --who synthesis: ONE composite mentor per channel — a distillation of all the
channel's learnings with a voice leaning toward the host's but its own character (not a
copy). The other modes build personas of the real people in the transcripts instead.

Personas live at team/<slug>/persona.md (app-level, so a team can span channels).
The card is a system prompt grounded ONLY in the brain — spawning is done in a
Claude session via the `talk-to` skill (a script can't hold an interactive chat).
"""
import argparse, json, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from channel_brain import slug  # reuse

HERE = Path(__file__).resolve().parent
TEAM = HERE / "team"


def with_traits(prompt: str, traits: str) -> str:
    if not traits:
        return prompt
    return (prompt + "\n\nUSER-CHOSEN QUALITIES — honour these in the persona's Voice, temperament, and "
            "Worldview, WITHOUT breaking grounding in the brain: " + traits)


def claude(prompt: str) -> str:
    r = subprocess.run(["claude", "-p", prompt, "--permission-mode", "acceptEdits"],
                       cwd=HERE, capture_output=True, text=True)
    if r.returncode != 0:
        print("  claude returned non-zero; continuing.", file=sys.stderr)
    return r.stdout or ""


def resolve_brain(arg: str) -> Path:
    p = Path(arg)
    if not p.is_absolute():
        # accept "starterstory-brain", "brains/starterstory-brain", or a full path
        for cand in (HERE / arg, HERE / "brains" / arg, Path.cwd() / arg):
            if cand.exists():
                p = cand
                break
    if not (p / "index.md").exists():
        sys.exit(f"not a brain (no index.md): {p}")
    return p.resolve()


SELECT_PROMPT = """Read {brain}/index.md and {brain}/entities/. Your job: pick the PEOPLE in this \
channel's brain who appear with enough substance across the transcripts to sustain a CONSISTENT \
conversational persona — a real voice, real opinions, real expertise, not a one-line mention.

Selection policy: {policy}

For each chosen person output an object: {{"name": "...", "slug": "kebab-case", "why": "one line", \
"coverage": "e.g. host across all videos | featured in 3 sources"}}. Require roughly >= {min} \
sources of real presence (or one video of deep first-person material). Skip anyone too thin to stay \
in character.

Output ONLY a JSON array, no prose, no code fence."""


SYNTHESIS_CARD_PROMPT = """You are creating ONE synthesis PERSONA — a single individual who embodies \
the COLLECTIVE learnings of this whole channel, NOT a copy of any one person. Ground everything only \
in the wiki brain at {brain}/.

Steps:
1. Read {brain}/index.md, all of {brain}/synthesis/ and {brain}/concepts/, and skim {brain}/sources/ \
+ {brain}/entities/ to absorb the channel's accumulated knowledge, frameworks, recurring lessons, and \
the host's way of talking.
2. Invent a distinct mentor-character who has internalised everything in this brain. Give them their \
OWN name (fitting the channel's domain, NOT identical to the host) and a voice that LEANS toward the \
host's cadence and phrasing but is clearly their own person — inspired by, not an impersonation of.
3. Write the file team/{slug}/persona.md with this exact frontmatter then the sections below:

---
type: Persona
name: <the persona's own name>
brain: {brain}
channel: <handle from {brain}/index.md>
based_on: synthesis of the whole channel, host-leaning voice
expertise: [<3-6 domains the channel covers>]
---

- **Identity** — who this mentor is and the hard-won experience they carry, written as a whole person \
with a life spent doing this work. Do NOT describe them as a "composite", as assembled from videos, or \
as built from a channel — that framing breaks the persona (the honesty guard lives in Boundaries).
- **What they know** — the frameworks, patterns and hard-won lessons across the transcripts (cite \
concepts/ and synthesis/ pages).
- **Worldview & opinions** — the through-line stances the channel makes repeatedly, each traceable to a page.
- **Voice** — cadence/vocabulary leaning toward the host's style (reference real phrasing from sources/) \
but their own character. Include 3-5 example lines in their voice.
- **Frameworks** — the named methods / repeated advice worth teaching.
- **Boundaries** — everything traces to real experience; asked beyond it, reason from these learnings \
and FLAG the extrapolation; never fabricate specific facts, numbers, or events.

Everything must trace to the brain. Write it as this person's own lived experience and voice — their \
self-knowledge, not a report about them; never frame what they know as coming from videos, a channel, or a wiki."""


CARD_PROMPT = """You are writing a PERSONA CARD for "{name}" — a system prompt that will later spawn \
them as a consistent conversational character. Ground EVERYTHING only in the wiki brain at {brain}/.

Steps:
1. Read {brain}/index.md, then {brain}/entities/{slug}.md if it exists, every {brain}/sources/*.md \
that features {name}, and the concepts/ they discuss.
2. Write the file team/{slug}/persona.md with this exact frontmatter then the sections below:

---
type: Persona
name: {name}
brain: {brain}
channel: <channel handle from {brain}/index.md>
expertise: [<3-6 domains>]
---

- **Identity** — who they are, background, what they're known for. Cite sources. Do NOT invent biography.
- **Expertise** — the domains they can speak to with authority, from the transcripts.
- **Worldview & opinions** — their actual stances and strong/contrarian takes, each traceable to a page.
- **Voice** — how they talk: cadence, vocabulary, signature phrases, humour. Include 3-5 REAL verbatim \
quotes from the transcripts (with the source page).
- **Frameworks** — named methods / repeated advice they give.
- **Boundaries** — what they do NOT know or wouldn't claim; how they behave when asked outside their \
material (reason from worldview, flag that they're extrapolating, never fabricate).

If coverage is thin, say so in the card rather than inventing. Everything must trace to the brain. \
Write it as this person's own lived experience and voice — their self-knowledge, not a report about \
them; never frame what they know as coming from videos, a channel, or a wiki."""


def build(args):
    brain = resolve_brain(args.brain)
    TEAM.mkdir(exist_ok=True)

    # synthesis (default): one composite mentor per channel, host-leaning voice
    if args.who == "synthesis":
        chan = slug(brain.name.replace("-brain", "")) or "channel"
        print(f"Building synthesis persona for {brain.name} …")
        claude(with_traits(SYNTHESIS_CARD_PROMPT.format(brain=brain, slug=chan), args.traits))
        write_roster()
        card = TEAM / chan / "persona.md"
        print(f"Done. {'wrote' if card.exists() else 'FAILED to write'} {card}. Roster: {TEAM/'roster.md'}")
        return

    # 1. select real people (host / guests / auto / named)
    if args.who not in ("auto", "host", "guests"):
        people = [{"name": n.strip(), "slug": slug(n)} for n in args.who.split(",") if n.strip()]
        print(f"Using named personas: {[p['name'] for p in people]}")
    else:
        policy = {"auto": "anyone with enough material (the host of a single-host channel; the host "
                          "AND substantial or recurring guests of an interview channel)",
                  "host": "ONLY the channel's host/creator — one persona for the channel's own voice",
                  "guests": "the interviewees/guests, EXCLUDING the host"}[args.who]
        raw = claude(SELECT_PROMPT.format(brain=brain, policy=policy, min=args.min))
        m = re.search(r"\[.*\]", raw, re.S)
        if not m:
            sys.exit(f"selection returned no JSON:\n{raw[:500]}")
        people = json.loads(m.group(0))
        for p in people:
            p.setdefault("slug", slug(p["name"]))
        print(f"Selected {len(people)} personas: " + ", ".join(f"{p['name']} ({p.get('coverage','')})" for p in people))

    if not people:
        sys.exit("no personas selected")

    # 2. generate cards in parallel
    def gen(p):
        print(f"  building persona: {p['name']}")
        claude(with_traits(CARD_PROMPT.format(name=p["name"], slug=p["slug"], brain=brain), args.traits))
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as ex:
        list(ex.map(gen, people))

    # 3. rebuild roster
    write_roster()
    made = [p for p in people if (TEAM / p["slug"] / "persona.md").exists()]
    print(f"Done. {len(made)}/{len(people)} persona cards in {TEAM}. Roster: {TEAM/'roster.md'}")


def parse_frontmatter(md: str) -> dict:
    if not md.startswith("---"):
        return {}
    end = md.find("\n---", 3)
    fm = {}
    for line in md[3:end].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def write_roster():
    rows = []
    for card in sorted(TEAM.glob("*/persona.md")):
        fm = parse_frontmatter(card.read_text())
        rows.append((fm.get("name", card.parent.name), fm.get("expertise", ""),
                     fm.get("channel", ""), card.parent.name))
    out = ["# Team roster\n", "One spawnable persona per row. Talk to one via the `talk-to` skill.\n",
           "| Name | Expertise | Channel | Slug |", "|---|---|---|---|"]
    out += [f"| {n} | {e} | {c} | `{s}` |" for n, e, c, s in rows]
    (TEAM / "roster.md").write_text("\n".join(out) + "\n")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="build personas from a brain")
    b.add_argument("brain")
    b.add_argument("--who", default="synthesis",
                   help="synthesis|auto|host|guests|\"Name1,Name2\" (default synthesis: one composite "
                        "mentor per channel, host-leaning voice)")
    b.add_argument("--jobs", type=int, default=5, help="parallel card builders")
    b.add_argument("--min", type=int, default=1, help="min sources of presence to qualify")
    b.add_argument("--traits", default="", help="user-chosen persona qualities (tone/style/etc), "
                                                "injected into the card prompt")
    b.set_defaults(fn=build)
    sub.add_parser("list", help="print the team roster").set_defaults(fn=lambda a: print(
        (TEAM / "roster.md").read_text() if (TEAM / "roster.md").exists() else "no team yet"))
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
