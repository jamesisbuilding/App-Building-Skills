---
name: app-keyword-research
description: Validate an app idea against the App Store before building it. Turns the idea into search phrases, measures demand (App Store autocomplete) and competition (current top-10 apps) for each, ranks keywords by opportunity, and maps which apps own the market. Use when the user wants keyword research, ASO, "is there demand for…", "who are the competitors for…", "what should we call it / which keywords", or to validate or compare app ideas.
---

# App keyword research

Answers three questions about an app idea from Apple's public App Store data, with no account or API key:

1. **Traffic:** are people searching for this, and with which words?
2. **Difficulty:** how hard is it to rank for those words?
3. **Market:** which apps own this space, how big are they, and how do they make money?

It ends in a verdict, the keywords to target, and an App Store title, subtitle and keyword field.

## Workflow

### 1. Turn the idea into 10–20 seed phrases

Seeds are the starting searches; the script expands each one through autocomplete. Cover:

- **The core job, in the user's words:** "mental math", "habit tracker" (not "numeracy enhancement").
- **Synonyms and alternative names:** "math game", "arithmetic", "times tables".
- **The audience:** "math games for adults", "… for kids". Separate audiences are separate markets.
- **Adjacent categories it competes with:** "brain training" for a maths app.
- **Outcome phrases:** "quick math", "math workout".

Don't seed with competitor brand names. They will show up in the results anyway, which is useful for the market map.

**Other countries get seeds in their own language.** Germans search what Germans type ("kalorienzähler", not "kalorien tracker"), so write each market's seeds from what locals would type and check them through autocomplete. Never translate the English winners and assume they hold.

**Second pass from the incumbents' titles.** After the first run, read the non-brand words in the market map's top apps (e.g. "cards", "tips" in "Mental Math Cards Games & Tips"). Developers converge on words that work, so the ones you haven't covered become a second batch of seeds, run into the same `--out`.

### 2. Run the research

```bash
python3 -I scripts/keyword_research.py \
  --seeds "mental math, math game, math games for adults, brain training, times tables" \
  --country us --max-terms 120 --out research/<idea>-us-<yyyy-mm-dd>
```

- **Runtime:** about 6 seconds per phrase at the start of a run, falling as the same apps keep ranking (their details are cached). 120 phrases take about 8–10 minutes, so run big batches in the background.
- **Progress:** results are saved as it goes. `report.md` is readable mid-run, and re-running into the same `--out` resumes.
- **Other options:**
  - `--seeds-file seeds.txt`: one phrase per line.
  - `--no-expand`: score only the seeds you give it.
  - `--country gb|de|jp|…`: the 52 main storefronts. Autocomplete and rankings differ by country, so research each launch market.
  - `--app-id <trackId>`: for a live app, fills the "Our rank" column (1–200, or 200+) for every phrase, at no extra cost. Re-run into dated folders to track rankings after a metadata change.
- **Outputs:**
  - `report.md`: the two tables below.
  - `keywords.json` and `apps.json`: raw data for follow-up questions.
- **Tests:** `python3 -I scripts/test_keyword_research.py` and `python3 -I scripts/test_check_metadata.py` run offline.

### 3. Read the keyword table

Each phrase gets three 0–100 heuristic scores:

| Score | How it's measured | Read it as |
|---|---|---|
| **Demand** | The fewer letters typed before App Store suggests the phrase, and the higher its slot, the more it's searched. Apple orders suggestions by search volume. | Letters ≤ 4: high. 5–7: medium. ≥ 8: low. Never suggested (score 0): unknown, below what autocomplete measures. |
| **Competition** | The median rating count of the current top 10 on a log scale, plus 2 points per top-10 app with the whole phrase in its name or subtitle (plurals, accents and compounds like "kalorienzähler" = "Kalorien Zähler" count; subtitles are only known for about the top 8). | Median < 1k: weak. 1k–20k: moderate. 20k–100k: strong. > 100k: owned by big brands. 5 or more exact titles means many apps target the phrase directly. |
| **Opportunity** | demand × (1 − competition / 100) | The sort order. The sweet spot is demand ≥ 60 with competition ≤ 55. |

The **Verdict** column turns those into one word: **target** (demand ≥ 40, competition ≤ 55: winnable for a new app), **hard** (competition > 55), **low** (demand < 40), **floor** (demand 0), **brand** (see below), and, with `--app-id`, **own** (your app is top 3) or **push** (top 10: close, worth reinforcing in the listing). It's a first sort, not the decision: the intent cut below still applies.

Patterns to call out:

- **High demand, weak competition: the opening.** Example: "mental math" (suggested after 4 letters, top-10 median 609 ratings).
- **High demand where no top-10 app has the whole phrase in its name or subtitle: a title opening,** even when competition is strong. Example: "math games for adults", median 112k ratings but 0/10 exact titles.
- **Autocomplete phrases that are brand names** ("times tables rock stars", "impulse brain training") belong to a competitor. List them in the market map, never in your keywords; Apple rejects metadata that uses other apps' trademarks. The script marks a phrase *(brand)* and lists it last when it's a top-10 app's whole title, because a tiny app's own name otherwise scores near-zero competition and tops the table. It can't catch brand phrases that only partly match a title ("impulse brain training"), and it can mark a generic phrase that some app took as its exact title ("percentage calculator"), so still read the list.
- **Audience-split phrases** ("… for 3rd grade", "… for adults") are different products. Say which segment the idea serves.
- **High demand but 0/10 exact titles is also a smell.** Either it's a real gap (rare) or the phrase is too vague for anyone to build on (common). Apply the intent test below before calling it an opening.

**Cut for intent before you rank.** The script can't judge this; you must. A keyword counts only when the person typing it expects an app like this one. Ask of each: *how many people typing this want THIS app?* Cut two classes that score deceptively well:

- **Too generic:** "tracker" for a calorie tracker. Huge demand, but the searcher may want sleep, budget or flight trackers.
- **Adjacent, wrong intent:** "muscle growth" for a calorie tracker. Related to the idea, but the searcher wants workout apps. You might even rank; the installs won't come, and those that do won't stay.

**Demand 0 means unknown, not zero.** Never suggested is below what autocomplete can measure (the same as popularity 5, the floor, in Apple Search Ads). One such phrase in the keyword field is a lottery ticket. The title and subtitle keywords must have clearly measurable demand; floor phrases are only filler after the proven ones are placed.

**Judge competition against the app's stage.**

- **New app:** target competition ≤ 55 for present-day rankings. A stronger phrase in the title is a bet on the future, so the keyword field must carry winnable phrases for now.
- **Established app** (thousands of ratings): competition up to about 70 becomes contestable, because ranking authority builds with installs and ratings.
- **A live app ranking ~100+ for a phrase in its own title or subtitle** (see `--app-id`) has an authority problem, not a keyword problem. More keywords won't fix it; installs and ratings will.

### 4. Read the market map

The second table lists the apps that appear in the top 10 for the most phrases: the incumbents. For the top 5–10:

- **Size:** a rating count in the hundreds of thousands means a funded leader, while thousands means indie-sized and beatable.
- **Freshness:** a last update more than a year ago means a stale leader, which is an opening.
- **Quality:** an average rating below about 4.3 means users are unhappy. Their reviews are a feature list for you.
- **Business model:** price is in the table. In-app purchases and subscription prices aren't in the API, but the store page embeds them. Fetch `https://apps.apple.com/us/app/id<trackId>` with curl, HTML-unescape it, and read the JSON after `"title":"In-App Purchases"`: each `textPair` is a product and its price, e.g. King of Math's `"Full Game"` / `"$3.99"`. A category where every leader charges a subscription proves people pay. A strong one-time-unlock rival sets the price anchor you'll be compared with.
- **Search dominance versus fame:** count how often each app is in the top 3 across all phrases (`keywords.json` → `top`). A famous rival can be absent from search. For example, King of Math (3k ratings, 15 years old) was in the top 3 for 0 of 178 maths phrases, while Mental Math Cards Games & Tips was in the top 3 for 41.

### 5. Deliver the verdict

Use this structure:

1. **Verdict:** go / go for a niche / avoid, in one sentence, with the reason.
2. **Sweet-spot keywords:** the top 5–10 by opportunity, each with its demand, competition and why it was picked.
3. **Segments:** a table of keyword clusters with demand, competition and what each means (as in the example below).
4. **Who owns the market:** the top incumbents, their size, freshness and business model.
5. **App Store metadata:**
   - **Title:** up to 30 characters. Keyword first, brand second: "Calorie Tracker — Glow Up" beats "Glow Up — Calorie Tracker", because people search the keyword, not an unknown brand, and earlier words weigh more. Brand-first is a choice the user makes knowingly, never the default.
   - **Subtitle:** up to 30 characters. The second-strongest keyword, written descriptively: "Track macros & lose weight" is a subtitle, "Feel amazing every day" wastes 30 characters.
   - **Keyword field:** up to 100 characters, comma-separated with no spaces. Don't repeat words already in the title or subtitle (Apple combines them), use singular forms, and leave out brand names and the app's category name.
   - **Apple product names** (iPhone, iPad, Apple Watch) in the title or subtitle are a rejection (guideline 5.2.5). In the keyword field they're fine, and worth it if the app really has, say, a Watch app.
   - **Check it:** `python3 -I scripts/check_metadata.py --title "…" --subtitle "…" --keywords "…"` fails on limits and Apple names, and warns on wasted characters.
   - Present it as a table: keyword, the surface it's assigned to (title, subtitle or keyword field), demand, competition, and a one-line intent argument. Get the user's explicit approval of the title and subtitle keywords before writing listings or localising anything from them.
   - Title, subtitle and keyword field only change with a new app version (promotional text is the only field editable live), so plan keyword changes to ride the next release.
6. **Caveats:** the limits below that apply.

## Limits (always state the relevant ones)

- **Demand is relative, not absolute.** Autocomplete position ranks phrases against each other; it gives no download counts. The true metric is Apple Search Ads popularity (5–100), available through an Apple Search Ads account or paid tools such as Astro.
- **Competition uses rating counts as a proxy for downloads.** It's correlated, but not the same.
- **Results are a snapshot.** Re-run into a dated folder to see trends.
- **The US App Store is the default.** Other countries need their own run.

## Astro (paid keyword tool), if it's installed

Astro (`/Applications/Astro.app`, bundle `matteospada.it.ASO`) provides the real Search Ads popularity and its own difficulty score. What was found about it (October 2026):

- **Demo limit:** the demo version allows 10 keywords per app, and popularity, difficulty and suggestions need a licence.
- **MCP server:** Astro has its own, documented at tryastro.app/docs/mcp, switched on from its home screen. It needs a licence. When it's licensed and running, prefer its tools for popularity and difficulty over the heuristics here. The workflow maps onto it:
  - Put a not-yet-released app's research in a temporary folder or tag, so it stays apart from live tracking.
  - Seeds: `get_keyword_suggestions`, plus `extract_competitors_keywords` on the 3–5 closest rivals (find them with `search_app_store`).
  - Per market: `search_rankings` on the local storefront shows who's winning there.
  - It also reports how many apps use a keyword in their name or subtitle. Many is evidence the phrase is searched; zero on a popular phrase is the smell described above.
- **Local data:** stored in `~/Library/Containers/matteospada.it.ASO/Data/Library/Application Support/Astro/Model.sqlite` (Core Data). Always copy the file and its `-wal` and `-shm` files before reading it.
  - Keywords are in `ZKEYWORD`: `ZTEXT`, `ZSTORE`, `ZPOPULARITY`, `ZDIFFICULTY`, `ZAPPSCOUNT`, `ZCURRENTRANKING`.
  - Timestamps are seconds since 2001, so add 978307200 for Unix time.
- **Don't call Astro's server (`api.tryastro.app`) directly.** Its popularity data is the licensed product. Use the app, its MCP server, or ask the user to add the keywords in Astro and then read the local database.
- **Driving its window from scripts is unreliable.** It's a SwiftUI app whose sidebar ignores scripted clicks, and screen capture needs a permission the terminal usually lacks.

## RankPilot (our own tracker), once the app is live

RankPilot is our local App Store keyword tracker (Node 22.5+, no dependencies, data in `~/.rankpilot/rankpilot.db`). This skill decides *what to target* before and at launch; RankPilot then *tracks* it: rank history per keyword and country, what moved since the last check, and which apps beat you. Hand over once the listing is live.

- **Its MCP tools** (`node bin/rp.js mcp install` registers them): `status`, `app_add` (yours or a competitor), `keywords_add`, `keywords_localize` (AI writes each market's local phrase), `check_run`, `board_get` (keywords × countries with rank, previous rank, volume, difficulty, verdict, and up to 5 apps beating you per country), `term_get` (one phrase explained, with the top 10 and their relevance), `keywords_brainstorm`.
- **Hand-over:** add the app with `app_add`, add the approved keywords (title, subtitle and keyword field) with `keywords_add`, set the local phrases this skill found per market with `phrase_set` rather than letting AI guess, then `check_run`.
- **Its volume is not demand.** RankPilot's volume is the audience (ratings) of the apps matching a phrase: proof that people use such apps, not that they search those words. This skill's autocomplete demand is the search signal. Use both: high volume with demand 0 means a big category searched in other words; high demand with low volume means searched but under-served.
- **Its difficulty adjusts for store size.** It scales the top-10 median by how big each country's store is compared with the US (from apps ranking in both), so a 1k-rating median in Germany reads harder than in the US. This skill doesn't, so read non-US competition as an underestimate.

## Gotchas

- **SSL:** Python from python.org on macOS often has no CA certificates, so `urllib` fails on every HTTPS request. The script uses `curl` for that reason. Keep it that way, and never swallow request errors silently.
- **Country header:** autocomplete and search need the `X-Apple-Store-Front` header as `<storefront>-<language>,29` (both IDs are in `STOREFRONTS` in the script). Without it, results default to the US. With the wrong language ID (the script used `-1`, English, everywhere until 31 October 2026) a German search answers in a different order and German competition reads lower than it is.
- **Two endpoints:** search uses the App Store's own endpoint (`MZStore.woa/wa/search`), which returns the real store order, ~200 ranks, and subtitles for about the top 8. The iTunes Search API's order differs slightly from what users see. App details (developer, price, last update) come from the iTunes lookup API.
- **Rate limit:** the iTunes lookup API allows about 20 requests a minute, so the script pauses 3.2 seconds after each lookup, looks up only apps it hasn't seen, and backs off on failure. Don't parallelise it.

## Example: 7 Minute Math (US, October 2026)

A daily 7-minute mental maths game for adults. Its key findings:

| Segment | Demand | Competition (top-10 median ratings) | Meaning |
|---|---|---|---|
| mental math | 4 letters | 609, 7/10 exact titles | Best opening: searched and weakly contested |
| mental math practice / trainer | 8 letters | 4–700 | Little demand, but nearly uncontested |
| math games for adults | 4 letters | 112k, 0/10 exact titles | Big demand, title opening |
| brain training | 7 letters | 108k–138k | Elevate, Peak, Lumosity, Impulse, all subscriptions: proves adults pay |
| times tables / grade-level maths | 5–7 letters | 2k–60k | Large, but kids and parents: a different product |

Verdict: go, positioned as mental maths for adults. Title around "mental math", subtitle around "brain training for adults", and freemium subscription pricing in line with the brain-training leaders.

## Extending this skill

Ideas to add over time, kept as separate scripts in `scripts/`:

- **Google Play:** the equivalent autocomplete and search scraping.
- **Apple Search Ads API:** real popularity scores once an account exists.
- **Review mining:** pull the incumbents' 1–3★ reviews (`https://itunes.apple.com/us/rss/customerreviews/id=<app id>/sortBy=mostRecent/json`, 50 per page; verified October 2026) to find unmet needs.
- **Trend tracking:** compare dated research folders for the same seeds.

The intent test, the demand floor, stage-based difficulty, keyword-first titles and the Astro mapping were adapted from [vibe-aso](https://github.com/Kronop/vibe-aso) (MIT), October 2026. The store-order search, the storefront table with language IDs, phrase matching in names and subtitles, and the verdicts come from RankPilot.
