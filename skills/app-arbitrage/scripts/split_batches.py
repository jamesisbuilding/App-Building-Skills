"""Split reviews.csv into JSONL batches for coder subagents. Usage: split_batches.py <reviews.csv> <out_dir> [batch_size=120] [--filter low|low+asks] [--since YYYY-MM]"""
import csv, json, pathlib, re, sys
src, out = sys.argv[1], pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
size = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 120
flt = sys.argv[sys.argv.index("--filter") + 1] if "--filter" in sys.argv else "all"
ask = re.compile(r"\b(wish|please|add|would love|would be nice|suggest|only (thing|con|complaint|issue)|missing|need[s]? )", re.I)
since = sys.argv[sys.argv.index("--since") + 1] if "--since" in sys.argv else ""
# keep i = CSV row index even when filtering, so code_stats can join back
rows = [dict(i=i, rating=int(r["rating"]), version=r.get("version", ""), title=r.get("title", ""), text=r["text"])
        for i, r in enumerate(csv.DictReader(open(src))) if r.get("date", "") >= since]
if flt != "all":  # big apps: code only what carries the signal, and say so in the report
    rows = [r for r in rows if r["rating"] <= 3 or (flt == "low+asks" and ask.search(r["text"]))]
for b in range(0, len(rows), size):
    (out / f"batch_{b // size:02d}.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows[b:b + size]) + "\n")
print(len(rows), "reviews in", -(-len(rows) // size), "batches ->", out)
