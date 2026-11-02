"""Merge coded JSONL with reviews.csv, validate, and print the evidence tables.
Usage: code_stats.py <reviews.csv> <coding_dir> [--md out.md] [--since YYYY-MM]

Validation: every coded i exists, no duplicates, quotes are exact substrings
(failures are listed, never silently fixed)."""
import collections, csv, json, pathlib, sys
src, cdir = sys.argv[1], pathlib.Path(sys.argv[2])
R = {i: r for i, r in enumerate(csv.DictReader(open(src)))}
C, bad = {}, []
for f in sorted(cdir.glob("coded_*.jsonl")):
    for n, line in enumerate(f.read_text().splitlines(), 1):
        if not line.strip(): continue
        try: c = json.loads(line)
        except json.JSONDecodeError: bad.append(f"{f.name}:{n} invalid JSON"); continue
        i = c.get("i")
        if i not in R: bad.append(f"{f.name}:{n} unknown i={i}"); continue
        if i in C: bad.append(f"{f.name}:{n} duplicate i={i}")
        q = (c.get("quote") or "").strip()
        if q and q not in R[i]["text"] and q not in R[i].get("title", ""): bad.append(f"i={i} quote not verbatim: {q[:60]}")
        C[i] = c
since = sys.argv[sys.argv.index("--since") + 1] if "--since" in sys.argv else ""
C = {i: c for i, c in C.items() if R[i].get("date", "") >= since}  # stale controversies swamp old reviews
expected = sum(1 for b in cdir.glob("batch_*.jsonl") for l in b.read_text().splitlines() if l.strip())
out = []
P = out.append
star = lambda i: int(R[i]["rating"])
band = lambda i: "1-2" if star(i) <= 2 else ("3" if star(i) == 3 else "4-5")
N = len(C)
P(f"# Coded evidence\n\nCoded {N} of {expected} batched reviews ({len(R)} in the CSV){' since ' + since if since else ''}. Validation issues: {len(bad)}.")
for b in bad[:30]: P(f"- {b}")

def table(title, counter, total, extra=None):
    P(f"\n## {title}\n\n| | n | % |" + (" " + extra[0] + " |" if extra else "") + "\n| --- | --- | --- |" + (" --- |" if extra else ""))
    for k, v in counter.most_common():
        P(f"| {k} | {v} | {100*v/total:.0f}% |" + (f" {extra[1](k)} |" if extra else ""))

# aspects: complaints and praise by star band
neg, pos = collections.Counter(), collections.Counter()
negb = collections.defaultdict(collections.Counter)
for i, c in C.items():
    for a, s in (c.get("aspects") or {}).items():
        (neg if s == "-" else pos)[a] += 1
        if s == "-": negb[a][band(i)] += 1
P("\n## Aspects\n\n| aspect | complaints | 1-2★ | 3★ | 4-5★ | praise |\n| --- | --- | --- | --- | --- | --- |")
for a in sorted(set(neg) | set(pos), key=lambda a: -(neg[a] + pos[a])):
    P(f"| {a} | {neg[a]} | {negb[a]['1-2']} | {negb[a]['3']} | {negb[a]['4-5']} | {pos[a]} |")

table("Payer status", collections.Counter(c.get("payer", "unknown") for c in C.values()), N,
      ("avg ★", lambda k: f"{sum(star(i) for i,c in C.items() if c.get('payer')==k)/max(1,sum(1 for c in C.values() if c.get('payer')==k)):.2f}"))
table("Concept", collections.Counter(c.get("concept", "0") for c in C.values()), N)
pers = collections.Counter(p for c in C.values() for p in (c.get("persona") or []) if p != "unknown")
def top_neg(p):
    k = collections.Counter(a for c in C.values() if p in (c.get("persona") or []) for a, s in (c.get("aspects") or {}).items() if s == "-")
    return ", ".join(f"{a} {n}" for a, n in k.most_common(3))
table("Personas (stated in text)", pers, N, ("top complaints", top_neg))
table("Requests", collections.Counter(r for c in C.values() for r in (c.get("requests") or [])), N)
table("Willingness to pay", collections.Counter(c.get("wtp", "unknown") for c in C.values()), N)
conds = [c["wtp_condition"] for c in C.values() if c.get("wtp") == "would_pay_if" and c.get("wtp_condition")]
P("\n## Would pay if\n\n" + "\n".join(f"- {x}" for x in conds))
table("Churn reasons (churned=true)", collections.Counter(c.get("churn_reason") or "unstated" for c in C.values() if c.get("churned")), max(1, N))
# severity-weighted pain: what to fix first
pain = collections.Counter()
for c in C.values():
    for a, s in (c.get("aspects") or {}).items():
        if s == "-": pain[a] += c.get("severity", 1)
table("Pain score (sum of severity on complaints)", pain, max(1, sum(pain.values())))
# timeline: complaint share by version for the top 5 pain aspects
top = [a for a, _ in pain.most_common(5)]
byv = collections.defaultdict(list)
for i, c in C.items(): byv[R[i].get("version", "")].append(c)
vkey = lambda v: [int(x) if x.isdigit() else 0 for x in v.split(".")]
P("\n## Timeline: share of reviews complaining, by version\n\n| version | n | avg ★ | " + " | ".join(top) + " |\n| --- | --- | --- |" + " --- |" * len(top))
for v in sorted(byv, key=vkey):
    cs = byv[v]
    if len(cs) < 8: continue
    avg = sum(star(i) for i in C if R[i].get("version") == v) / len(cs)
    P(f"| {v} | {len(cs)} | {avg:.2f} | " + " | ".join(f"{100*sum(1 for c in cs if (c.get('aspects') or {}).get(a)=='-')/len(cs):.0f}%" for a in top) + " |")
# multi-app runs: sources look like "<app>:appstore-us"
apps = collections.defaultdict(list)
for i, c in C.items():
    if ":" in R[i]["source"]: apps[R[i]["source"].split(":")[0]].append(c)
if apps:
    P("\n## By app\n\n| app | coded | top complaints | top requests |\n| --- | --- | --- | --- |")
    for a, cs in sorted(apps.items(), key=lambda x: -len(x[1])):
        k = collections.Counter(x for c in cs for x, s in (c.get("aspects") or {}).items() if s == "-")
        q = collections.Counter(x for c in cs for x in (c.get("requests") or []))
        P(f"| {a} | {len(cs)} | " + ", ".join(f"{x} {n}" for x, n in k.most_common(5)) + " | " + ", ".join(f"{x} {n}" for x, n in q.most_common(5)) + " |")
text = "\n".join(out)
if "--md" in sys.argv: pathlib.Path(sys.argv[sys.argv.index("--md") + 1]).write_text(text)
print(text)
