#!/usr/bin/env python3
"""App Store keyword research from Apple's public data. No account or API key needed.

For each seed phrase it collects App Store autocomplete suggestions (real searched phrases), then
scores every phrase for:
  demand       how few letters you type before App Store suggests it, and its slot in the list
               (Apple ranks suggestions by search volume; suggested after 3-4 letters = heavily searched)
  competition  median rating count of the current top-10 apps, and how many carry the whole phrase
               in their name or subtitle (the strongest ranking signals)
It also builds a market map: the apps that keep appearing in the top 10 across all phrases.

Usage:
  keyword_research.py --seeds "mental math, math game, brain training" --out research/
  keyword_research.py --seeds-file seeds.txt --country gb --max-terms 60 --out research/

Writes <out>/keywords.json, <out>/apps.json and <out>/report.md, saving as it goes so a long run
can be read part-way through. Re-running with the same --out resumes: phrases already scored are skipped.

Searches use the App Store's own search endpoint (store order, ranks up to ~200, subtitles), the one
RankPilot uses. App details come from the iTunes lookup API, which allows roughly 20 requests a minute,
so each phrase that brings new apps costs ~3 s more; apps already seen are cached. Budget ~6 s per
phrase at the start of a run, falling as the same apps keep ranking.
"""
import argparse, json, math, os, plistlib, re, statistics, subprocess, sys, time, unicodedata, urllib.parse

# (storefront ID, language ID) for the X-Apple-Store-Front header: autocomplete and search are per
# country, and the language ID makes them answer in the country's language (table from RankPilot)
STOREFRONTS = {
    "us": (143441, 1), "gb": (143444, 2), "ca": (143455, 6), "au": (143460, 27), "nz": (143461, 27),
    "ie": (143449, 2), "in": (143467, 2), "sg": (143464, 2), "de": (143443, 4), "at": (143445, 4),
    "ch": (143459, 57), "fr": (143442, 3), "be": (143446, 2), "nl": (143452, 10), "lu": (143451, 2),
    "it": (143450, 7), "es": (143454, 8), "pt": (143453, 24), "se": (143456, 17), "no": (143457, 2),
    "dk": (143458, 2), "fi": (143447, 2), "pl": (143478, 2), "cz": (143489, 2), "sk": (143496, 2),
    "hu": (143482, 2), "ro": (143487, 2), "hr": (143494, 2), "si": (143499, 2), "gr": (143448, 2),
    "tr": (143480, 2), "ua": (143492, 2), "ru": (143469, 16), "il": (143491, 2), "jp": (143462, 9),
    "kr": (143466, 13), "cn": (143465, 19), "tw": (143470, 18), "hk": (143463, 45), "th": (143475, 2),
    "vn": (143471, 2), "id": (143476, 2), "my": (143473, 2), "ph": (143474, 2), "pk": (143477, 2),
    "br": (143503, 15), "mx": (143468, 28), "ar": (143505, 28), "co": (143501, 28), "cl": (143483, 28),
    "ae": (143481, 2), "sa": (143479, 2)}


def get(url, headers=()):
    """curl rather than urllib: macOS python.org builds often lack CA certificates, which made
    every urllib request fail. Raises on any HTTP or network failure."""
    cmd = ["curl", "-sf", "--max-time", "20"] + [x for h in headers for x in ("-H", h)] + [url]
    return subprocess.run(cmd, capture_output=True, check=True).stdout


class Research:
    def __init__(self, country):
        self.country = country
        self.store = "X-Apple-Store-Front: {}-{},29".format(*STOREFRONTS[country])
        self.hint_cache, self.details = {}, {}

    def hints(self, prefix):
        """App Store autocomplete for a prefix, most searched first."""
        if prefix in self.hint_cache:
            return self.hint_cache[prefix]
        url = ("https://search.itunes.apple.com/WebObjects/MZSearchHints.woa/wa/hints?clientApplication=Software&term="
               + urllib.parse.quote(prefix))
        for attempt in range(3):
            try:
                terms = [h["term"] for h in plistlib.loads(get(url, [self.store])).get("hints", [])]
                self.hint_cache[prefix] = terms
                time.sleep(0.25)
                return terms
            except Exception as e:
                print(f"  hints {prefix!r} failed ({e}), retrying", file=sys.stderr)
                time.sleep(2 * (attempt + 1))
        self.hint_cache[prefix] = []
        return []

    def demand(self, term):
        """(letters typed before App Store suggests the term, its 1-based slot), or (None, None)."""
        for k in range(2, len(term) + 1):
            h = self.hints(term[:k])
            if term in h:
                return k, h.index(term) + 1
        return None, None

    def lookup(self, ids):
        """iTunes details for app ids, cached for the run. Missing ids (not sold here) are skipped."""
        need = [i for i in ids if i not in self.details]
        if need:
            url = "https://itunes.apple.com/lookup?" + urllib.parse.urlencode(
                {"id": ",".join(need), "country": self.country, "entity": "software"})
            for attempt in range(4):
                try:
                    for x in json.loads(get(url))["results"]:
                        self.details[str(x["trackId"])] = x
                    time.sleep(3.2)  # the iTunes API allows ~20 requests a minute
                    break
                except Exception as e:
                    print(f"  lookup failed ({e}), backing off", file=sys.stderr)
                    time.sleep(10 * (attempt + 1))
            else:
                raise RuntimeError("iTunes lookup kept failing")
        return self.details

    def search(self, term):
        """Live App Store search in store order: (up to ~200 app ids, top-10 details with subtitles),
        or None if it keeps failing."""
        url = ("https://search.itunes.apple.com/WebObjects/MZStore.woa/wa/search?clientApplication=Software"
               "&caller=com.apple.AppStore&term=" + urllib.parse.quote(term))
        for attempt in range(4):
            try:
                data = json.loads(get(url, [self.store]))
                bubbles = data["pageData"]["bubbles"]
                ids = list(dict.fromkeys(str(r["id"]) for r in (bubbles[0]["results"] if bubbles else [])))[:200]
                lockups = data.get("storePlatformData", {}).get("native-search-lockup", {}).get("results", {})
                time.sleep(0.35)
                details = self.lookup(ids[:10])
                break
            except Exception as e:
                print(f"  search {term!r} failed ({e}), backing off", file=sys.stderr)
                time.sleep(10 * (attempt + 1))
        else:
            return None
        top = []
        for i in ids[:10]:
            lock = lockups.get(i, {})
            x = dict(details.get(i) or {"trackId": int(i), "trackName": lock.get("name", ""),
                                         "userRatingCount": (lock.get("userRating") or {}).get("ratingCount", 0)})
            x["subtitle"] = lock.get("subtitle") or ""  # only the top ~8 come with one
            top.append(x)
        return ids, top


def demand_score(letters, slot):
    """0-100. Suggested after 2 letters in slot 1 = 100; each extra letter costs 12, each slot 2."""
    if letters is None:
        return 0
    return max(0, 100 - (letters - 2) * 12 - (slot - 1) * 2)


def competition_score(median_ratings, in_title):
    """0-100. Log scale of the top-10 median rating count (500k+ = 100), plus up to 20 for
    exact-phrase titles (apps that target the phrase directly are hard to outrank)."""
    base = min(100, math.log10(median_ratings + 1) / math.log10(500_000) * 80)
    return round(min(100, base + in_title * 2))


def opportunity(d, c):
    return round(d * (1 - c / 100))


def _tokens(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    return re.findall(r"\w+", "".join(c for c in s if not unicodedata.combining(c)))


def _same(a, b):
    return a == b or (len(a) > 3 and a == b + "s") or (len(b) > 3 and b == a + "s")


CJK_THAI = re.compile(r"[\u0e00-\u0e7f\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af]")


def matches(term, *texts):
    """True when a name or subtitle carries the whole phrase: its words in sequence (accents and plurals
    aside), as one compound ("kalorienzähler" = "Kalorien Zähler"), or as a substring for CJK and Thai."""
    p = _tokens(term)
    if not p:
        return False
    for text in texts:
        if CJK_THAI.search(term):
            if "".join(p) in "".join(_tokens(text)):
                return True
            continue
        t = _tokens(text)
        if any(all(i + j < len(t) and _same(t[i + j], w) for j, w in enumerate(p)) for i in range(len(t))):
            return True
        if len("".join(p)) >= 8 and "".join(p) in "".join(t):
            return True
    return False


def verdict(r):
    """One word per phrase: own / push (your app is top 3 / top 10), brand, floor (demand unmeasurable),
    low (demand < 40), target (competition <= 55, winnable for a new app) or hard."""
    if r.get("brand"):
        return "brand"
    if r["demand"] and r.get("our_rank") and r["our_rank"] <= 10:
        return "own" if r["our_rank"] <= 3 else "push"
    if not r["demand"]:
        return "floor"
    if r["demand"] < 40:
        return "low"
    return "target" if r["competition"] <= 55 else "hard"


def is_brand(term, titles):
    """True when the phrase is a top-10 app's whole title, punctuation aside: autocomplete is
    suggesting that app by name, and its tiny rating count would otherwise fake an opening."""
    norm = lambda s: " ".join(re.findall(r"\w+", s.lower()))
    return norm(term) in {norm(t) for t in titles}


def write_report(out, rows, apps, args):
    rows = sorted(rows, key=lambda r: (bool(r.get("brand")), -r["opportunity"]))
    lines = [f"# Keyword research ({args.country.upper()} App Store)", "",
             f"Seeds: {', '.join(args.seed_list)}  ",
             f"{len(rows)} phrases scored. Demand and competition are 0-100 heuristics (see SKILL.md); "
             "opportunity = demand × (1 − competition/100). Phrases marked *(brand)* are a top-10 app's "
             "exact title, listed last: competitors to note, never keywords to use.", "",
             "## Keywords by opportunity", "",
             "| Keyword | Verdict | Opportunity | Demand | Letters | Slot | Competition | Median ratings | Exact in name/subtitle | #1 app | Our rank |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        rank = r.get("our_rank") or ("200+" if args.app_id else "–")
        lines.append(f"| {r['term']}{' *(brand)*' if r.get('brand') else ''} | {verdict(r)} | {r['opportunity']} | {r['demand']} | {r['letters'] or '–'} | {r['slot'] or '–'} | "
                     f"{r['competition']} | {r['median_ratings']:,} | {r['exact_in_title']}/10 | {r['top'][0]['name'] if r['top'] else ''} | {rank} |")
    ranked = sorted(apps.values(), key=lambda a: (-a["appearances"], -a["ratings"]))
    lines += ["", "## Market map: apps that keep ranking", "",
              "Apps appearing in the top 10 for the most phrases own this market.", "",
              "| App | Subtitle | Developer | Top-10 appearances | Ratings | Avg | Price | Genre | Released | Last update |",
              "|---|---|---|---|---|---|---|---|---|---|"]
    for a in ranked[:30]:
        lines.append(f"| [{a['name']}]({a['url']}) | {a.get('subtitle', '')} | {a['developer']} | {a['appearances']} | {a['ratings']:,} | "
                     f"{a['avg_rating']:.1f} | {a['price']} | {a['genre']} | {a['released'][:10]} | {a['updated'][:10]} |")
    open(os.path.join(out, "report.md"), "w").write("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seeds", help="comma-separated seed phrases")
    ap.add_argument("--seeds-file", help="one seed phrase per line")
    ap.add_argument("--country", default="us", choices=sorted(STOREFRONTS))
    ap.add_argument("--max-terms", type=int, default=120, help="cap on phrases scored (runtime ~3-6 s each)")
    ap.add_argument("--no-expand", action="store_true", help="score only the seeds, skip autocomplete expansion")
    ap.add_argument("--app-id", help="your live app's trackId: records its rank (1-200) for every phrase")
    ap.add_argument("--out", required=True, help="output folder")
    args = ap.parse_args()

    seeds = [s.strip().lower() for s in (args.seeds or "").split(",") if s.strip()]
    if args.seeds_file:
        seeds += [l.strip().lower() for l in open(args.seeds_file) if l.strip() and not l.startswith("#")]
    if not seeds:
        ap.error("give --seeds or --seeds-file")
    args.seed_list = seeds
    os.makedirs(args.out, exist_ok=True)
    kw_path, apps_path = os.path.join(args.out, "keywords.json"), os.path.join(args.out, "apps.json")

    # Resume a previous run into the same folder
    rows = json.load(open(kw_path)) if os.path.exists(kw_path) else []
    apps = json.load(open(apps_path)) if os.path.exists(apps_path) else {}
    done = {r["term"] for r in rows}

    r = Research(args.country)
    pool = []
    for s in seeds:
        for t in [s] + ([] if args.no_expand else r.hints(s)):
            if t not in pool:
                pool.append(t)
    pool = pool[: args.max_terms]
    todo = [t for t in pool if t not in done]
    print(f"{len(pool)} phrases ({len(done)} already scored), ~{len(todo) * 5 // 60 + 1} min", file=sys.stderr)

    for i, term in enumerate(todo, 1):
        letters, slot = r.demand(term)
        found = r.search(term)
        if found is None:
            print(f"[{i}/{len(todo)}] {term}: search failed, skipped", file=sys.stderr)
            continue
        ids, res = found
        our_rank = ids.index(args.app_id) + 1 if args.app_id in ids else None
        counts = [x.get("userRatingCount", 0) for x in res]
        median = int(statistics.median(counts)) if counts else 0
        in_title = sum(matches(term, x["trackName"], x["subtitle"]) for x in res)
        d, c = demand_score(letters, slot), competition_score(median, in_title)
        rows.append({"term": term, "letters": letters, "slot": slot, "demand": d, "median_ratings": median,
                     "exact_in_title": in_title, "competition": c, "opportunity": opportunity(d, c), "our_rank": our_rank,
                     "brand": is_brand(term, [x["trackName"] for x in res]),
                     "top": [{"name": x["trackName"], "ratings": x.get("userRatingCount", 0)} for x in res[:3]]})
        for x in res:
            a = apps.setdefault(str(x["trackId"]), {
                "name": x["trackName"], "developer": x.get("sellerName", ""), "url": x.get("trackViewUrl", ""),
                "ratings": x.get("userRatingCount", 0), "avg_rating": x.get("averageUserRating", 0) or 0,
                "price": x.get("formattedPrice", ""), "genre": x.get("primaryGenreName", ""),
                "released": x.get("releaseDate", ""), "updated": x.get("currentVersionReleaseDate", ""),
                "appearances": 0, "keywords": []})
            a["subtitle"] = a.get("subtitle") or x["subtitle"]
            a["appearances"] += 1
            a["keywords"].append(term)
        print(f"[{i}/{len(todo)}] {term}: demand {d}, competition {c}, opportunity {rows[-1]['opportunity']}",
              file=sys.stderr)
        json.dump(rows, open(kw_path, "w"), indent=1)
        json.dump(apps, open(apps_path, "w"), indent=1)
        write_report(args.out, rows, apps, args)

    write_report(args.out, rows, apps, args)
    print(f"done: {os.path.join(args.out, 'report.md')}", file=sys.stderr)


if __name__ == "__main__":
    main()
