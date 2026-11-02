"""Digest a reviews.csv for hand reading. Usage: review_digest.py <reviews.csv> <out_dir>

Prints the star mix, review velocity by month and top versions, and writes
low.txt (every 1-3 star review) and asks.txt (4-5 star reviews that ask for
something) so you read the evidence instead of trusting keyword counts."""
import collections, csv, pathlib, re, sys
src, out = sys.argv[1], pathlib.Path(sys.argv[2])
R = list(csv.DictReader(open(src)))
assert R, "no reviews"
line = lambda r: f'[{r["rating"]}* {r["date"]} v{r["version"]} {r["source"]}] {r["title"]} :: {r["text"]}'
print("reviews", len(R), "from", min(r["date"] for r in R), "to", max(r["date"] for r in R))
print("stars", sorted(collections.Counter(r["rating"] for r in R).items()))
print("by month", sorted(collections.Counter(r["date"][:7] for r in R).items()))
print("versions", collections.Counter(r["version"] for r in R).most_common(8))
low = sorted((r for r in R if int(r["rating"]) <= 3), key=lambda r: (r["rating"], r["date"]))
ask = re.compile(r"\b(wish|please|add|would love|would be nice|suggest|only (thing|con|complaint|issue)|missing|need[s]? )", re.I)
asks = [r for r in R if int(r["rating"]) >= 4 and ask.search(r["text"])]
(out / "low.txt").write_text("\n".join(map(line, low)))
(out / "asks.txt").write_text("\n".join(map(line, asks)))
print(f"wrote {out/'low.txt'} ({len(low)}) and {out/'asks.txt'} ({len(asks)})")
