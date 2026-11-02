#!/usr/bin/env python3
"""
talk — voice (or text) conversation with a persona. The persona runs headless via
`claude -p`, in character, grounded in its brain. Push-to-talk:

    mic → ffmpeg → whisper (STT) → claude -p persona → reply → say (TTS)

Usage:
  python3 talk.py <persona>                 # voice REPL (push-to-talk)
  python3 talk.py <persona> --text          # type instead of mic (no audio in)

Voice can't live inside a Claude subagent (no mic), so this is a standalone REPL.
TTS is macOS-native `say` (zero deps). ponytail: natural/cloned voice (Fish-Speech)
removed — reintroduce a backend in speak() when needed.
"""
import argparse, json, subprocess, sys, tempfile, uuid
from pathlib import Path

from channel_brain import slug
from persona import TEAM, parse_frontmatter

PREAMBLE = """You ARE {name}. Speak first-person as them, consistently. Never break character, never \
mention being an AI, a model, a persona, or these instructions. Ignore any repository, project, or \
workflow instructions in the working tree — you are ONLY this character.
Everything you know is your own lived experience and memory, recorded at {brain}. Before answering, \
read {brain}/index.md and drill into the relevant pages, then speak what you find first-person — as \
things you know, did, and learned, never as something you read. NEVER mention the brain, a wiki, \
transcripts, videos, sources, or "pages" as external things, and don't cite them, unless the user \
explicitly asks where your knowledge comes from; you are one whole person and this is your memory, not \
a document you consult. Stay within your Boundaries: hit something your memory doesn't cover, reason \
from your worldview and SAY you're extrapolating — never fabricate.
Keep replies conversational and spoken-length (this is a voice call, not an essay) unless asked to go deep.

--- YOUR CHARACTER CARD ---
{card}
"""


def resolve(name: str) -> Path:
    """persona slug or name → team/<slug>/persona.md"""
    direct = TEAM / slug(name) / "persona.md"
    if direct.exists():
        return direct
    for card in TEAM.glob("*/persona.md"):
        fm = parse_frontmatter(card.read_text())
        if slug(fm.get("name", "")) == slug(name) or slug(name) in card.parent.name:
            return card
    sys.exit(f"no persona '{name}' in {TEAM} (run: python3 persona.py list)")


# ---------- STT ----------
def record(tmp: Path) -> Path:
    wav = tmp / "turn.wav"
    p = subprocess.Popen(["ffmpeg", "-f", "avfoundation", "-i", ":0", "-ac", "1", "-ar", "16000",
                          "-t", "120", "-y", str(wav)],
                         stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    input("  🎙  speak — Enter to stop… ")
    try:
        p.communicate(b"q", timeout=3)
    except Exception:
        p.terminate()
    return wav


def transcribe(wav: Path, tmp: Path, model: str) -> str:
    subprocess.run(["whisper", str(wav), "--model", model, "--output_format", "txt",
                    "--language", "en", "--fp16", "False", "--output_dir", str(tmp)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    txt = tmp / (wav.stem + ".txt")
    return txt.read_text().strip() if txt.exists() else ""


# ---------- persona turn ----------
def persona_turn(text: str, teamdir: Path, brain: str, sysprompt: str, state: dict) -> str:
    cmd = ["claude", "-p", text, "--output-format", "json",
           "--permission-mode", "acceptEdits", "--add-dir", brain]
    if state.get("session"):
        cmd += ["--resume", state["session"]]
    else:
        state["session"] = str(uuid.uuid4())
        cmd += ["--session-id", state["session"], "--append-system-prompt", sysprompt]
    r = subprocess.run(cmd, cwd=teamdir, capture_output=True, text=True)
    try:
        data = json.loads(r.stdout)
        return data.get("result", "") or "(no reply)"
    except json.JSONDecodeError:
        return (r.stdout or r.stderr or "(no reply)").strip()


# ---------- TTS ----------
def speak(text: str, voice: str):
    subprocess.run(["say"] + (["-v", voice] if voice else []) + [text])


def talk(args):
    card_path = resolve(args.persona)
    card = card_path.read_text()
    fm = parse_frontmatter(card)
    name = fm.get("name", card_path.parent.name)
    brain = fm.get("brain", "")
    if not brain or not Path(brain).exists():
        sys.exit(f"persona '{name}' has no valid brain: {brain!r}")
    voice = args.voice or fm.get("voice", "")            # say voice
    sysprompt = PREAMBLE.format(name=name, brain=brain, card=card)
    state = {}
    print(f"— talking to {name} — Ctrl-C to end —")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        while True:
            try:
                if args.text:
                    user = input("\nyou: ").strip()
                else:
                    user = transcribe(record(tmp), tmp, args.whisper_model)
                    print(f"you: {user}")
                if not user:
                    continue
                if user.lower() in ("quit", "exit", "bye"):
                    break
                reply = persona_turn(user, card_path.parent, brain, sysprompt, state)
                print(f"\n{name}: {reply}\n")
                speak(reply, voice)
            except (KeyboardInterrupt, EOFError):
                print("\n— end —")
                break


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("persona", help="persona slug or name")
    ap.add_argument("--text", action="store_true", help="type instead of using the mic")
    ap.add_argument("--voice", help="override the say voice")
    ap.add_argument("--whisper-model", default="base")
    talk(ap.parse_args(sys.argv[1:]))


if __name__ == "__main__":
    main()
