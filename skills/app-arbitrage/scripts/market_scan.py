"""Top-10 App Store search results per term: who owns it and how big. Usage: market_scan.py <cc> term1 term2 ..."""
import datetime, json, subprocess, sys, urllib.parse
cc, terms = sys.argv[1], sys.argv[2:]
cutoff = (datetime.date.today() - datetime.timedelta(days=548)).isoformat()  # young = launched in the last 18 months
for t in terms:
    u = f"https://itunes.apple.com/search?term={urllib.parse.quote(t)}&country={cc}&entity=software&limit=10"
    res = json.loads(subprocess.run(["curl", "-sf", "--max-time", "20", u], capture_output=True, text=True).stdout or '{"results":[]}')["results"]
    top = sorted(res, key=lambda r: -r.get("userRatingCount", 0))
    med = sorted(r.get("userRatingCount", 0) for r in res)[len(res)//2] if res else 0
    young = [r for r in res if r["releaseDate"] >= cutoff and r.get("userRatingCount", 0) >= 500]
    print(f"\n## {t}  (median ratings {med:,}; young hits {len(young)})")
    for r in res[:6] + [r for r in res[6:] if r in young]:
        print(f'  {r.get("userRatingCount",0):>9,}  {r.get("averageUserRating",0):.1f}  {r["releaseDate"][:7]}  {r["formattedPrice"]:>6}  {r["trackName"][:55]}')
