"""Combine per-app review CSVs into one market.csv with an app prefix. Usage: combine_market.py <market_dir>

Reads <market_dir>/<app>.csv (from rip_reviews.py), writes <market_dir>/market.csv with
source "<app>:appstore-xx" and title "[<app>] ..." so coders and code_stats.py know the app."""
import csv, pathlib, sys
d = pathlib.Path(sys.argv[1]); rows = []
for f in sorted(d.glob("*.csv")):
    if f.name == "market.csv": continue
    for r in csv.DictReader(open(f)):
        r["source"] = f"{f.stem}:{r['source']}"; r["title"] = f"[{f.stem}] {r['title']}"; rows.append(r)
with open(d / "market.csv", "w", newline="") as o:
    w = csv.DictWriter(o, fieldnames=["source", "url", "date", "rating", "version", "title", "text"]); w.writeheader(); w.writerows(rows)
print(len(rows), "reviews ->", d / "market.csv")
