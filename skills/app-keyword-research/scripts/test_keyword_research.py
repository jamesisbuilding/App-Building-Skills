#!/usr/bin/env python3
"""Offline checks for the scoring heuristics:  python3 -I scripts/test_keyword_research.py"""
import os, runpy

kr = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "keyword_research.py"))
demand, competition, opportunity = kr["demand_score"], kr["competition_score"], kr["opportunity"]

# Demand: earlier and higher in autocomplete = more searched; never suggested = 0
assert demand(2, 1) == 100
assert demand(4, 4) == 70  # "mental math" (US, Oct 2026)
assert demand(None, None) == 0
assert demand(12, 10) == 0  # floors at 0

# Competition: log-scaled median ratings plus exact-title saturation, capped at 100
assert competition(0, 0) == 0
assert competition(500_000, 0) == 80
assert competition(500_000, 10) == 100
assert competition(609, 7) < competition(112_570, 0)  # small niche beats a giant market

# Opportunity: the 2026 maths research ranked "mental math" above "math games for adults"
assert opportunity(demand(4, 4), competition(609, 7)) > opportunity(demand(4, 7), competition(112_570, 0))

# Brand: a phrase that is a top-10 app's whole title (Germany, Oct 2026), but not a generic part of one
is_brand = kr["is_brand"]
assert is_brand("iqora: iq-test & gehirnjogging", ["IQora: IQ-Test & Gehirnjogging", "Peak"])
assert is_brand("iq boost – gehirnjogging", ["IQ Boost –  Gehirnjogging"])  # dash and spacing differ
assert not is_brand("mental math", ["Mental Math Cards Games & Tips", "Mental Math: Speed Training"])

# Matching a phrase in a name or subtitle (ported from RankPilot's relevance rules)
matches = kr["matches"]
assert matches("mental math", "Mental Math Cards Games & Tips")
assert matches("math game", "Brain Training", "Fun Math Games")  # subtitle, plural
assert matches("kalorienzähler", "Kalorien Zähler")  # compound
assert matches("calculo mental", "Cálculo Mental")  # accents
assert matches("暗算", "暗算トレーニング")  # Japanese, no spaces
assert not matches("math", "Aftermath")
assert not matches("mental math", "Math Mental Gym")  # words out of order
assert not matches("", "Anything")

# Verdict: rank beats demand, brand beats everything, floor is unknown not zero
verdict = kr["verdict"]
row = lambda **k: {"demand": 70, "competition": 50, "brand": False, "our_rank": None, **k}
assert verdict(row()) == "target"
assert verdict(row(competition=71)) == "hard"
assert verdict(row(demand=30)) == "low"
assert verdict(row(demand=0)) == "floor"
assert verdict(row(our_rank=2)) == "own" and verdict(row(our_rank=8)) == "push"
assert verdict(row(brand=True, our_rank=1)) == "brand"
print("ok")
