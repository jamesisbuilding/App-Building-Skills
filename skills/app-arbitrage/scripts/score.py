"""Rank rebuild candidates from candidates.json. Usage: score.py <candidates.json> [--md out.md]

Each candidate (fill from the coded evidence and market scans, never from guesses):
  name                 short label
  evidence_reviews     coded reviews (target app + market apps) that ask for this or are the left-out persona
  evidence_wtp         of those, how many are would_pay_if / pays_happy
  market_ratings       sum of US ratings of the top 3 incumbents serving this audience/content
  incumbents_charge    true if a top incumbent sells a subscription (people already pay here)
  format_entrants      apps already doing this mechanic for this audience/content
  entrants_traction    how many of those have 1,000+ ratings
  build                "S" | "M" | "L"
  distribution         1-5: cheap reach (communities, creators, ad interests), with a reason in notes
  licensing_ok         false kills it (content we cannot legally ship)
  review_risk          "low" | "med" | "high" (4.3 copycat, kids category, health claims)
  notes                one line

The score is a confidence ranking, not a probability. Weights below; change them only with a reason."""
import json, math, pathlib, sys
W = dict(evidence=25, wtp=10, market=20, pays=10, room=15, distribution=10, build=5, risk=5)
C = json.loads(pathlib.Path(sys.argv[1]).read_text())
assert C, "no candidates"
maxe = max(c["evidence_reviews"] for c in C) or 1
def parts(c):
    if not c.get("licensing_ok", True): return None
    room = 1.0 if c["format_entrants"] == 0 else (0.7 if c["entrants_traction"] == 0 else max(0.0, 0.5 - 0.2 * (c["entrants_traction"] - 1)))
    return dict(
        evidence=c["evidence_reviews"] / maxe,
        wtp=min(1.0, c["evidence_wtp"] / max(1, c["evidence_reviews"]) * 2),
        market=min(1.0, math.log10(max(10, c["market_ratings"])) / 6),  # 1M ratings = full marks
        pays=1.0 if c["incumbents_charge"] else 0.3,
        room=room,
        distribution=(c["distribution"] - 1) / 4,
        build={"S": 1.0, "M": 0.6, "L": 0.2}[c["build"]],
        risk={"low": 1.0, "med": 0.5, "high": 0.0}[c["review_risk"]])
rows = []
for c in C:
    p = parts(c)
    rows.append((-1 if p is None else sum(W[k] * v for k, v in p.items()), c, p))
rows.sort(key=lambda r: -r[0])
out = ["| rank | candidate | score /100 | " + " | ".join(W) + " | notes |", "| --- | --- | --- | " + "--- | " * len(W) + "--- |"]
for n, (s, c, p) in enumerate(rows, 1):
    cells = " | ".join(f"{W[k]*p[k]:.0f}" for k in W) if p else " | ".join("-" for _ in W)
    out.append(f"| {n} | {c['name']} | {'KILLED (licensing)' if p is None else f'{s:.0f}'} | {cells} | {c.get('notes','')} |")
text = "\n".join(out)
if "--md" in sys.argv: pathlib.Path(sys.argv[sys.argv.index("--md") + 1]).write_text(text)
print(text)
