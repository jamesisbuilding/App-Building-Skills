---
name: app-arbitrage
description: >-
  App in, highest-confidence rebuild suggestion out. Takes an existing,
  successful App Store app, pulls its metadata and every review Apple's public
  feed exposes (36 storefronts, both sort orders), has subagents tag every
  review against a codebook (payer status, concept, persona, aspects,
  requests, willingness to pay, churn, severity, verbatim quote), validates
  candidate tweaks against the reviews of the apps already serving each
  candidate market, scores the candidates with a fixed rubric, and writes the
  teardown, the evidence tables and a seeded features.csv for Zero to
  Shipped. Use when the user pastes an App Store link and says "analyse this
  app", "rip the reviews", "app arbitrage", "how do we make a better
  version", "find tangential markets", "teardown", "sentiment analysis on the
  reviews", or "what should we rebuild".
---

# app-arbitrage

Copying an app is not the play. The play is the version of it that the
evidence says people will choose over it: fixing what every app in the
space gets wrong, for an audience or with content the original does not
serve. This skill turns one App Store link into that decision, with counts
you can check.

Worked example (read it before the first run):
`~/Desktop/Side Projects/App SOP/teardowns/scroll-the-bible/`.

## Rules

- **Never fabricate.** Counts come from script output. Quotes are verbatim
  (`code_stats.py` fails any quote that is not an exact substring).
- **Official feeds only.** iTunes Lookup/Search APIs and Apple's customer
  reviews RSS. No scraping libraries against stores. Reddit/TikTok by hand
  in the browser, if at all.
- **Research, not copying.** Never reuse the original's name, icon,
  screenshots, listing copy or artwork. App Review 4.3 rejects copycats and
  near-duplicate apps; 5.2 covers IP. Variants for different audiences go in
  one app as a setting, not as several apps.
- **Reviewers are not testimonials.** Their words never go in our listing.
- **Check content licensing** for every candidate: public domain, licensable
  (and at what cost), or ours to generate.
- Spend, ads, outreach and store submissions go to the user.

## Setup

Work in `teardowns/<slug>/` (App SOP folder) or `./teardown/<slug>/`.
Scripts: `~/.claude/skills/app-arbitrage/scripts/`, Python 3 + `curl`, run
with `python3 -I`. `S=~/.claude/skills/app-arbitrage` below.

| Script | Does |
| --- | --- |
| `rip_reviews.py <id> <out.csv>` | every review the RSS feed exposes, 36 storefronts x 2 sorts, deduped; prints ratings per storefront |
| `review_digest.py <csv> <dir>` | star mix, velocity by month, versions; writes `low.txt`, `asks.txt` for reading |
| `market_scan.py <cc> <terms...>` | top results per term with ratings, launch month, median, young hits (last 18 months, 500+ ratings) |
| `combine_market.py <dir>` | merges `<dir>/<app>.csv` into `market.csv` with app prefixes |
| `split_batches.py <csv> <dir> [size] [--filter low+asks] [--since YYYY-MM]` | JSONL batches for coder subagents |
| `code_stats.py <csv> <dir> [--since YYYY-MM] [--md out.md]` | validates and merges codes; aspects by star band, payer, concept, personas, requests, would-pay-if, churn, pain score, version timeline, per-app table |
| `score.py <candidates.json> [--md out.md]` | ranks candidates on the fixed rubric |

## Step 1: understand the app

```bash
curl -s "https://itunes.apple.com/lookup?id=<ID>&country=us"
curl -s "https://itunes.apple.com/lookup?id=<ARTIST_ID>&entity=software&country=us"
```

Record category, release date, version cadence, languages, price model, the
full description and release notes, the developer's other apps. Look at the
screenshots. Then write: **core loop**, **monetisation** (paywall placement,
trial, real prices, which reviews will confirm), **growth engine** (ad mentions
in reviews, review velocity by month, rating prompts), and **why it works**
in one sentence.

## Step 2: rip and read

```bash
python3 -I $S/scripts/rip_reviews.py <ID> reviews.csv
python3 -I $S/scripts/review_digest.py reviews.csv .
```

Read all of `low.txt` and `asks.txt` yourself. This is where you learn the
vocabulary for the codebook and the surprises (broken promises, false-choice
paywalls, whole groups left out).

## Step 3: codebook

Copy `$S/codebook.template.json` to `codebook.json`. Keep the generic
fields. Fill `aspects` (15-25, one line each, covering every theme you read,
both praise and complaint), `personas` (only groups that state themselves:
denominations, ages, parents, languages, low vision, low income...) and
`requests` (the named features from `asks.txt`). Good codebooks are concrete
("one verse per swipe in chapter mode"), not abstract ("UX").

## Step 4: tag every review

```bash
python3 -I $S/scripts/split_batches.py reviews.csv coding 125
```

Spawn one `general-purpose` subagent per batch, **in one message, model
`sonnet`**, at most ~9 at a time (re-batch bigger if needed: 230 per batch is
fine). Prompt each with:

> Follow the instructions in `$S/coder_prompt.md` with {CODEBOOK} =
> <abs path to codebook.json>, {BATCH} = <abs path to batch_NN.jsonl>,
> {OUT} = <abs path to coding/coded_NN.jsonl>. Do not modify any other file.

Then:

```bash
python3 -I $S/scripts/code_stats.py reviews.csv coding --md coded-evidence.md
```

Validation issues must be 0 (fix or re-run the batch). **Spot-check 10
random codes against the text yourself** and report the hit rate. Read each
coder's hand-back for judgment calls and tighten `coder_prompt.md` if two
coders disagree on a rule.

What to take from the tables:

- **Concept +/-**: if most reviewers like the idea, the business model or
  execution is the opening, not the idea.
- **Payer x stars**: who is angry (people who left at the paywall vs paying
  users) decides whether the fix is acquisition or retention.
- **Aspect complaints from 4-5 star reviewers**: happy users asking for
  something = upsell lever.
- **Would pay if**: the free/paid line, in users' words.
- **Churn reasons and pain score**: what to fix first.
- **Timeline**: which release changed sentiment (a paywall move, a bug).

## Step 5: crowding and neighbours

```bash
python3 -I $S/scripts/market_scan.py us "<main keyword>" "<mechanic> <content>" "<category>" ...
```

How many straight clones exist, and did any grow? Did the ones that grew
change the mechanic? Which young hits sit next door (they prove the channel)?

## Step 6: candidates

List 4-6 candidates from three sources:

- **Fix-the-model**: the original with everything the evidence says users
  hate fixed (often the strongest).
- **New audience**: each left-out persona.
- **Transplant**: the same mechanic on different content or for a different
  job (other faiths, languages, philosophy, blocking, audio).

## Step 7: validate each candidate in its own market

For every candidate audience, find the top 3-7 apps already serving it
(`market_scan.py`, then search for ids), rip their reviews into `market/`,
one CSV per app (`market/<app>.csv`), then combine them with an app prefix:

```bash
python3 -I $S/scripts/combine_market.py market
```

Write `market/codebook.json` for that market (include requests that would
confirm each candidate, e.g. `scroll_or_swipe_format`, `catholic_translation`).
Code only the signal, and only the recent past:

```bash
python3 -I $S/scripts/split_batches.py market/market.csv market/coding 230 --filter low+asks
python3 -I $S/scripts/code_stats.py market/market.csv market/coding --since <24 months ago> --md market/coded-evidence.md
```

The `--since` cut matters: one old controversy can fill an app's 1 star
reviews (Laudate 2021). Ask of each candidate market: do its users ask for
what we would build? What do they hate that we can fix? Do they pay?

## Step 8: score

Count each candidate's evidence from the coded files (a short Python filter
over `coded_*.jsonl`: personas, requests, aspects that support it, and how
many of those are `pays_happy` or `would_pay_if`). Fill `candidates.json`
(fields documented at the top of `score.py`), then:

```bash
python3 -I $S/scripts/score.py candidates.json --md scores.md
```

Rubric weights: evidence 25, would-pay 10, market size 20, incumbents
already charge 10, room (format entrants and their traction) 15,
distribution 10, build 5, review risk 5. Licensing that cannot be cleared
kills a candidate. Do not tune weights to get the answer you want; if the
ranking feels wrong, say why in the report.

Recommend the top candidate, and fold in cheap wins from the runners-up as
settings or ad angles rather than separate apps.

## Step 9: write it up

`teardown.md`, sections: 1 What it is · 2 What users love · 3 What users
hate · 4 What's missing · 5 Groups it leaves out · 6 Competitors · 7
Tangential markets · 8 The tweak (score table, recommendation, v1
must-haves, don't-copy list, licensing, validation test with kill numbers)
· 9 Next steps. Lead with sample sizes and what was not covered.

`features.csv` in the house format (`feature,area,priority,original,clone,notes`;
`original=yes` = in scope for v1) so `replica-diff/parity.py` can gate the
build.

**Validation test (always):** a landing page per ad angle (the winner plus
one or two runners-up as angles), about £150 each on Meta/TikTok, kill if
click-to-signup is under 15% or cost per signup is over £1.50. This is the
real probability check; the score only decides what to test first.

## Lessons from runs so far

- Straight clones of a hit stall. The follower that grows changes the
  mechanic (BibleScroll: blocking, not a feed).
- The original's growth engine is usually paid social; check review
  velocity. A good product without that channel goes nowhere (three Quran
  scroll apps, near zero ratings).
- Keyword counts mislead (substring matches, inflated personas). The tagged
  pass demoted the first pass's recommendation. Always tag.
- Billing and trial failures are often category-wide (Hallow's top
  complaint too), so honesty itself is a feature we can sell.

## Then

Zero to Shipped: 02/03 RankPilot and VOC depth → 04 the ad test → 05
`/app-offer` → 06 `/replica-brand` → 07 design → 08 `/create-app`.
