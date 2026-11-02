"""Pull every review Apple's public RSS feed exposes for an app, across storefronts. Usage: rip_reviews.py <app_id> <out.csv>"""
import csv, json, subprocess, sys, time
APP, OUT = sys.argv[1], sys.argv[2]
STORES = "us gb ca au nz ie za in ng ke gh ph sg my mx es ar co cl pe br de fr it nl se no dk fi pl pt ch at be jm tt".split()
def get(url):
    for _ in range(3):
        # curl, not urllib: python.org builds on macOS often lack CA certs
        try: return json.loads(subprocess.run(["curl", "-sf", "--max-time", "20", url], capture_output=True, text=True).stdout)
        except Exception: time.sleep(1)
    return {}
rows, seen = [], set()
for cc in STORES:
    meta = get(f"https://itunes.apple.com/lookup?id={APP}&country={cc}").get("results", [])
    if not meta: continue
    n0 = len(rows)
    for sort, page in [(s, p) for s in ("mostrecent", "mosthelpful") for p in range(1, 11)]:  # feed caps at 10 pages per sort
        entries = get(f"https://itunes.apple.com/{cc}/rss/customerreviews/page={page}/id={APP}/sortby={sort}/json").get("feed", {}).get("entry", [])
        if isinstance(entries, dict): entries = [entries]
        entries = [e for e in entries if "im:rating" in e]
        if not entries: continue
        for e in entries:
            rid = e["id"]["label"]
            if rid in seen: continue
            seen.add(rid)
            rows.append(dict(source=f"appstore-{cc}", url=f"https://apps.apple.com/{cc}/app/id{APP}?see-all=reviews", date=e["updated"]["label"][:10],
                             rating=e["im:rating"]["label"], version=e.get("im:version", {}).get("label", ""), title=e["title"]["label"], text=e["content"]["label"].replace("\n", " ")))
    print(cc, "ratings:", meta[0].get("userRatingCount"), "avg:", round(meta[0].get("averageUserRating", 0), 2), "reviews pulled:", len(rows) - n0, flush=True)
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["source", "url", "date", "rating", "version", "title", "text"]); w.writeheader(); w.writerows(rows)
print("total", len(rows))
