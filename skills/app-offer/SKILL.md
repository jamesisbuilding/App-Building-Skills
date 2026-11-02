---
name: app-offer
description: Designs one opinionated "Grand Slam Offer" for any app idea, new or already shipped, by running Alex Hormozi's $100M Offers method adapted to app stores. It covers the market and niche, the commodity check, a value-equation audit, the problem inventory, delivery vehicles, the trimmed value stack, pricing and tiers, scarcity, urgency, bonuses, the guarantee, naming, the paywall per placement, the onboarding fast win, a test plan and a ship plan. It works within App Store and Google Play rules. For a shipped app it reads the code and notes first and produces a before/after. Use it when the user says "/app-offer", "run app-offer on <idea>", "make a grand slam offer for my app", "Hormozi my app", "price my app" or "design my paywall offer", or asks how to package, price, name, guarantee or paywall an app. It writes offer/grand-slam-offer.md (or ./<app-slug>-grand-slam-offer.md for a new idea).
---

# app-offer

Run it once, end to end. Write one recommended offer to a file and put the alternatives in its appendix.

## Files

| File | When to read it |
|---|---|
| `reference/frameworks.md` (F§) | When a step says "Read F§n". Book frameworks with app translations, rubrics and examples; F§16 lists ideas judged not applicable; F§17 holds the runner formulas. |
| `reference/app-store-constraints.md` (C§) | Before steps 7, 8 and 9, and before you write any price, claim, timer, guarantee or name. It has an "as of" date. Re-verify anything that will ship. |
| `reference/100m-offers-transcript.txt` | Optional. Grep it for a detail. The skill must work without it. Never quote more than 15 consecutive words. |

## Hard rules (every step)

1. **Honest only.** No fake timers, counts or scarcity; no fake, AI-written or unattributed reviews or testimonials, and disclose any incentive behind one; no invented "was" prices or reasons; no hidden renewal terms; no features that are not in the build. Breaking this gets apps rejected (Apple 2.3.1, 5.6; Google Deceptive Behavior) and breaks EU/UK/FTC rules (C§7, C§8).
2. **Every dollar value needs a rationale**: hours saved x the user's hourly value, the price of the real-world alternative, or a real standalone price. No rationale, no number. Unvalued items count as zero in every ratio. Never pad a number to pass a test.
3. **The billed amount is the most prominent price.** Per-day or per-month equivalents are small and secondary (C§2).
4. **Flag these risks wherever they appear:**
   - Outcome + deadline claims: ad networks restrict them (C§7); App Review removes claims the app can't deliver or substantiate (2.3.1).
   - Health, cognitive, money or income claims need substantiation (C§7). Claim only measured in-app skill gains, not transfer to work, school or the brain.
   - Kids or teens: Kids Category, parental gate, COPPA, and the state age acts, which apply to under-18 users in any category (C§10).
   - Sensitive data (financial, health, intimate, location): C§16.
5. **A guarantee must be payable on every platform and every plan it is shown next to** (C§5).
6. **Market > offer > persuasion.** Fix the highest weak link first.
7. **Paraphrase the book.** Quote at most 15 words at a time, and rarely.
8. **Ask at most 3 questions**, only if the target user or core job can't be inferred; one of them may also bundle the founder numbers in Step 0.7 when the acquisition channel is unknown. Otherwise tag assumptions [A], benchmark stand-ins from C§14 [B], and keep going.
9. **Connectors:** don't query analytics or revenue connectors unless the user confirms the project or app ID belongs to this app. Otherwise ask or mark [A].
10. **Style and length:** plain and direct, tables for rubrics, no filler. Body about 3,000-4,000 words plus tables; overflow goes to the appendices.

## Step 0: Intake and assumptions

1. **Classify the input:** one sentence / doc / URL / existing repo. The working directory is this app's project only if the input names it or its code and notes match the idea. Otherwise treat the input as a new idea: don't grep the working directory, and write to `./<app-slug>-grand-slam-offer.md`.
2. **Existing app: ground in the evidence before designing anything.**
   - Products and prices: `grep -rniE 'purchases_flutter|revenuecat|Purchases\.|offering|entitlement|productId|product_id|weekly|annual|lifetime|StoreKit|BillingClient' --include='*.dart' --include='*.swift' --include='*.kt' --include='*.ts' --include='*.tsx' --include='*.json' --include='*.storekit' --exclude-dir={build,Pods,.dart_tool,node_modules,.git} .`
   - Paywall and onboarding: files named `*paywall* *onboard* *intro* *upgrade* *pro* *premium*`, plus localized copy (`.arb`, `.strings`, `strings.xml`). Record the shipped locales.
   - Analytics: `track(`, `logEvent`, Mixpanel/Amplitude/Firebase calls; note which of paywall_view, trial_start, purchase, cancel and retention events exist.
   - Notes: `CLAUDE.md`, `README*`, `docs/`, `research/`, memory files, `fastlane/metadata`, `CHANGELOG`, and files matching `*brand* *voice* *tone* *style* *listing* *aso* *keyword* *mascot* *pricing* *monetis* *paywall` (images too).
3. **Evidence mode.** With WebSearch/WebFetch: spend about 12 lookups on 5-10 competitors' prices and ratings, 1-3 star review themes for the top 3, and one community thread; cite URL and date in Appendix B. Without web: tag each item [A: memory, unverified] and list it under "To verify before pricing". No live data: use named C§14 rows as [B] stand-ins (refund rate = category refund row; paid periods per F§17.1; traffic = installs x share reaching the paywall). Pre-launch: review mining is "n/a: pre-launch"; mine competitors' reviews instead.
4. **Current offer** in the book's three parts: what they get, how they pay, the terms (F§1.2). New idea: "before" = the idea as stated (bare feature, no offer).
5. **Existing app: audit** the current paywall and onboarding against C§2, C§7 and C§8 (dismiss, disclosures, labelled estimates, implied outcomes, badges). List violations in §0. They ship first, regardless of the offer.
6. **Prior decisions** found in notes or memory become constraints in §0, each marked keep or challenge (with a reason). Never override one silently; put the challenger in Appendix A.
7. **Founder numbers** (defaults [A]): revenue goal ($100k/yr fee-net); acquisition channel (organic); build capacity (solo, part-time); store fee (15% if Small Business Program, else 30%; Google per C§1); VAT share of gross (from storefront mix, else 8%); income-tax rate (30%); avatar hourly value (local median wage); paywall views per week (measured, else 300).
8. **Flags:** child or teen users; health, cognitive or money claims; sensitive data; variable cost per user (inference, human minutes, SMS, third-party data or API fees such as bank aggregation, OCR or KYC, storage); multi-user product (couple, family, team, class: who must join for value, who pays); possible misuse against a vulnerable user (coercion, monitoring, minors).

Writes §0, plus the "before" column used in §11 and §12.

## Step 1: Starving-crowd market test (Read F§2)

| Test | 1 | 3 | 5 | Evidence |
|---|---|---|---|---|
| Pain | Nice-to-have, nobody complains | Recurring annoyance | Desperate, costly or embarrassing; raised unprompted | Competitor 1-3 star reviews, Reddit, search terms |
| Purchasing power | Payer can't pay (kids, unemployed) | Mixed | Payer has money and a reason (career, exam, health, parent) | Payer vs user, storefront mix, user-geography LTV (C§14) |
| Easy to target | No gathering place, no keyword | Some channels | Own keyword cluster, communities, creators; a custom product page could speak only to them | ASA keyword popularity, subreddits, creators |
| Growing | Shrinking, or about to be absorbed by the OS or free AI | Flat | Tailwind (demographic, platform, season, regulation) | Category trends, "Sherlock" risk |

- Map the app to **health, wealth or relationships**. Pure entertainment: say so; pain-based pricing is weaker there.
- **Score candidates:** the market as stated (existing app: the rung the current listing and brand serve) plus 2-4 sub-groups.
- **Verdict.** It judges the market as stated (existing app: the rung the current listing and brand serve). Check in this order:
  1. **PIVOT**: no candidate has every test at 3+. Say it plainly; the offer can't fix it.
  2. **GO**: the market as stated has every test at 3+ and a total of 14+. **GO (normal market)**: it has every test at 3+, a total of 12-13, and no sub-group with every test at 3+ scores higher; the offer carries it (F§2.7).
  3. **NICHE DOWN**: otherwise. Take the highest-scoring sub-group with every test at 3+; state its score, whether it reaches GO, the gap and what would close it.
- **Existing app on NICHE DOWN:** keep the main paywall on the current rung unless the user asks to reposition. Add the sub-group as an onboarding goal track, a custom product page and its own Offering; promote it only after its content ships and it wins a test.
- Rate **market / offer / persuasion** as great / normal / bad. State where effort goes first.
- **Niche ladder:** 4 rungs from generic to hyper-specific, with the price implication of each. Expect roughly a 2-5x premium across the ladder, not the book's 100x (F§16). The rung you commit to is the market as stated on GO, else the NICHE DOWN sub-group (existing app: the rule above).
- **Avatar:** 4 concrete qualifiers, who it is NOT for, and who could be harmed by the product or its misuse (and which offer elements become opt-in or excluded).
- **Positioning:** "We help [avatar] get [result] through [unique mechanism] without [deepest fear]."
- **TAM:** reachable payers x LTGP per payer = ceiling. New idea: provisional LTGP = category median annual price x (1 - fee) x (1 - VAT share) x 1.3 periods [A]; recompute in Step 7 and update §1.3 if the verdict changes. Plan an adjacent niche only if the computed ceiling, not a plateau, is below the goal; a plateau means improve the offer first.
- **Commit.** Other avatars become custom product pages or onboarding tracks later. Don't hop niches after one failed test.

Writes §1.

## Step 2: Commodity check (Read F§1.6, F§4.10, F§4.12)

- List at least 5 substitutes including the free ones: 2-3 named rival apps, YouTube/TikTok, ChatGPT or another free AI, the OS feature, pen and paper / a book / a tutor, and doing nothing. Gather prices and review themes per Step 0.3.
- Table: substitute | money cost | time to outcome | effort | dream / likelihood / time / effort scored 0, 0.5 or 1 (1 = favours the buyer: big dream, high likelihood, short time, low effort) | total /4 | why someone picks it.
- Answer: (1) How does a prospect compare these in store search (icon, screenshot 1, rating, price)? (2) Where does this app win on time or effort? Fast beats free. (3) What one sentence makes it a **category of one** (named method + avatar + outcome + interval)? If it needs explaining, it fails.

Writes §2.

## Step 3: Value equation audit (Read F§4)

Value = (Dream outcome x Perceived likelihood) / (Time delay x Effort and sacrifice). Score each driver 1-5; higher is always better, so time and effort score on how small they are. Calibrate to the app's natural cadence (daily game, weekly budget, monthly report); F§4.11 has examples for three app types.

| Driver | App measure | 1 | 5 |
|---|---|---|---|
| Dream outcome | The outcome as the user's peers or partner would notice it | A feature ("Unlock Pro") | A specific result plus an interval, in a scene that matters to the user's peer group or partner |
| Likelihood | Rating and count, measured outcome stats, personal baseline, personalised plan, demo of the result, fit signals, risk reversal | No proof | Baseline + "people like you" data + plan + guarantee |
| Time delay | Time to first felt win; a measured gain before the trial ends or the first renewal; visible progress | No felt win before the first charge | Felt win inside the first session (target in seconds); measured gain before the trial ends |
| Effort & sacrifice | Taps, typing, account, setup, permissions, minutes per cycle, willpower, embarrassment | Account + setup + permission walls before value; long sessions | Only the steps the core job truly needs, none before value; mistakes stay private |

- For every driver at 3 or less, list **logical** fixes (change the build) and **psychological** fixes (progress bars, plan screen, next-unlock countdown, per-day framing, renaming). Try psychological first; they're cheaper.
- Push the denominator toward zero: what would the done-for-you version be?
- Name the long-term dream and the benefits people stay for, with milestones at the app's cadence (e.g. day 1 / 3 / 7 / 30).

Writes §3 (before scores; after scores added in Step 11).

## Step 4: Problem inventory (Read F§7.2)

1. Walk the journey: discover > store page > install > onboarding > first session > (multi-user: invite sent > second user joins) > day 2 > first week > plateau or boredom > billing and renewal > life events (travel, busy week, new phone, shared device) > sharing > the next problem after success.
2. At each stage check four buckets: not worth it (dream); won't work for me / I won't stick with it (likelihood); too hard / I'll look stupid (effort); too slow / no time (time).
3. Write each obstacle in the user's own limiting-belief words. Mine reviews, Reddit, support email, cancellation reasons, onboarding drop-off (pre-launch: competitors' reviews).
4. Tag each with its driver. Aim for 20+; 30-60 is normal. Rank by frequency x severity.

Body: the top 25 rows (# | stage | user's words | driver | source). The rest go to Appendix D.

Writes §4.

## Step 5: Solutions and delivery vehicles (Read F§6, F§7.3-7.8)

1. Flip each problem into "How to [benefit] even if [obstacle]". Body shows the top 10; the rest go to Appendix D.
2. List vehicles for **every** problem: at least 3 for each of the top 10 and at least 1 for each of the rest, before judging any (diverge, then converge). Group problems that share a vehicle. Use the delivery cube:

| Axis | Options |
|---|---|
| Attention | 1:1 (founder, human coach, AI tutor) / small group (friend duel, family league, cohort) / 1:many (feature, content, leaderboard, live event) |
| Effort | DIY tool / DWY guided plan or AI coach / DFY automation |
| Medium | In-app, widget, notification, watch, lock screen / Live Activity, email, chat, voice, live session, printable |
| Response speed | Instant 24/7 (software, AI) / same day / weekly |

3. Brick exercise: change one attribute at a time (surface, format, session length, social size, audience, payer) and note new ideas.
4. 10x / 1/10 test: what would you deliver at 10x the price? How would users still win at 1/10? Keep the best idea from each end.

Writes §5: problem | how-to line | vehicles (cube codes).

## Step 6: Trim and stack (Read F§7.9-7.12)

Table (only vehicles that survive a first-pass cut): vehicle | build days | maintenance (both platforms, x locales for copy or content) | marginal cost per user per month (Step 0.8 list) | drivers moved | value H/M/L | decision.

- Cut high-cost/low-value first, then low-cost/low-value. Keep low-cost/high-value for Pro.
- Keep high-cost/high-value for the top tier only, with capped seats, or step it back a notch (daily human > weekly AI check-in > monthly auto report). If it needs a credential (financial, medical, legal), name a licensed partner and its cost; the founder never delivers regulated advice.
- Prefer assets built once and used by everyone: generators, adaptive plans, packs.
- **Coverage check:** each §4 problem must be removed by something real (a kept vehicle, mode, template or pack). Onboarding, paywall or FAQ copy can only point to it. List any uncovered.
- **Stack** survivors into 3-5 named bundles: a benefit-carrying name, a one-line benefit, the problems it kills, a $ value with its rationale.
- Stated values live in the offer doc, on web pages and in your conviction. Never print an invented "worth $X" total on a store paywall; use honest comparisons ("less than one tutoring session").
- List what the founder does by hand for the first 100 payers (overdeliver first, systematise later).

Writes §6.

## Step 7: Price (Read F§3, F§1.9-1.13, F§17.1; C§1-4, C§11, C§14)

1. **Unit economics per plan.** LTGP = price x (1 - store fee) x (1 - VAT share) x average paid periods - variable cost. Estimate paid periods per F§17.1 [B]. Variable cost includes revenue-share tools (RevenueCat, C§1); model the 95th-percentile user. Max CAC ≈ LTGP / 3. Report two cash numbers: proceeds earned by day 30 (accrual) vs CAC, and cash in the bank by day 75 for runway (payouts lag, C§1).
2. **Price position.** The book's default is premium leader: above the highest comparable app with a visibly different stack (F§3.10). For apps, start in the top quartile or at the top of the category; any lower position needs a written reason (store-search price sensitivity, ranking strategy). Never second-cheapest. Annualised price = hero price x billing periods per year. Compare each plan with the same-period C§14 median, else its annualised equivalent; compare lifetime with 2-3 years of the hero. If C§14 lacks the category, say so and use the all-category row plus live competitor prices.
3. **Value / price:** aim for 10x stack value against the annualised price. Consumer apps under ~$200/yr: report the honest ratio; 5x+ is acceptable. Below that, list the value additions that would close the gap. Add value; don't discount.
4. **Tiers:**

| Tier | Job | Contents | Delivery |
|---|---|---|---|
| Free | Trust engine, habit, proof | Enough to win once per natural cycle (day, week or month) | DIY, 1:many |
| Pro | Fastest route to the outcome | The bundles | DWY, personalised |
| Top (optional) | The top ~20% who would pay 5x+ | A scarce human or AI-heavy element, capped seats | 1:1 or small group |

   - Price the top tier at 5-10x annualised Pro. On iOS, real-time 1:1 human sessions may bill outside IAP (3.1.3(d)); one-to-few and one-to-many must use IAP. Google Play has no such exemption: use Play Billing, or in the US an enrolled program with its fees (C§11).
   - **Multi-user:** price per user or per household. Family Sharing is iOS-only and same-family; across platforms, grant the second member access through your own account entitlement on the backend (C§12).
5. **Period mix and anchoring.** Hero: annual (or longest subscription), pre-selected, with a trial. Alternative: one short plan (weekly or monthly). Anchor: lifetime or the top tier, also upfront cash. The onboarding paywall shows hero + alternative, with the anchor behind "More plans" or as a visually smaller third; contextual and milestone paywalls show the anchor openly. Weekly converts best but retains worst (C§14).
6. **Growth levers:** pick the cheapest to move: more payers (conversion), more per purchase (price, plan mix, top tier), or more purchases (retention, packs or add-ons lifetime buyers can still buy).
7. **Add bonuses instead of discounting.** Discounts only for dated seasonal events and win-back.
8. **Regional prices** from user-geography LTV (C§14). Don't block countries.
9. **Price-rise protocol:** raise value first; raise for new users only; grandfather existing users as a price lock; announce a dated lock-in window; respect consent thresholds and raise at most once in 12 months (C§4).
10. **New products:** any new IAP product or ads may be a "significant change" under the state app-store acts (C§10). Ship the age-signal integration first and notify the stores.
11. **First $100k:** units of each plan needed. Label the counts "fee-net revenue at shelf price, before VAT removal and income tax; App Store Connect proceeds will be lower in VAT storefronts". For take-home, also divide by (1 - VAT share) and (1 - tax rate) (F§14.1).

Writes §7. Price grid: plan | billed price | period | trial | LTGP | role.

## Step 8: Enhancers (Read F§8-13, F§17.2; C§3, C§5-8)

For each enhancer write what it is, why it is honest, and a compliance note.

**8a Scarcity: real limits only.**
- Honest sources: human time; inference cost; seats in a cohort, community or live event; a limited cosmetic or badge run; offer-code redemption caps; a grandfathered price lock. A founding batch is honest only with a real, lasting benefit (a locked price before a planned rise, a permanent perk) and a cap that never reopens.
- Price-lock wording must match store mechanics: on Apple say "lost if you stay unsubscribed for more than 60 days", never "gone the moment you cancel". No Android loss claim until Google's legacy-cohort behaviour is checked (C§4).
- Counts come from a real tally. No backend: enforce the cap by switching the Offering by hand and show the cap without a live count, or serve a count from a RevenueCat webhook to a serverless function (F§17.4).
- Never apply scarcity to the core subscription. If nothing is honestly limited, write "none".

**8b Urgency: at least one real deadline.**
- Options: an intro-offer window dated in the store console; a cohort or challenge start date; a named seasonal promo from a 12-month calendar, paired with a real in-app event; a price-rise date; a win-back window; the user's own date captured in onboarding (exam, wedding, move, tax day, trip).
- Every timer points at a fixed end date (server, RevenueCat Offering metadata or remote config) that never resets.
- Let bonuses expire, not the product.

**8c Bonuses: 3-5.**
- Each is named with its benefit, kills one named §4 objection or solves the next problem, says how it was made with proof, and carries a real value rationale.
- Tools, templates and generators beat more content.
- Total bonus value should exceed the core only where bonuses have real standalone prices. Otherwise show coverage instead (each top-5 objection killed by a bonus or bundle) and report the dollar test as FAIL rather than pad it.
- Mark which bonuses show on the paywall and which are the post-purchase "wow".
- Optional partner bonus: a non-competing app via an offer code, no user data shared.
- Never share-to-unlock, rate-to-unlock, or expiring credits.

**8d Guarantee.**
- List the fears, then pick a family:
  - unconditional: trial + reminder before the first charge + easy cancel. State cancel-anytime and the store refund route as plain information, never as your named guarantee (legal rights can't be sold as a feature, C§8); a named guarantee must add something you control.
  - conditional: outcome by a date; the conditions are your activation actions.
  - anti: you add no refund of your own on top of the store's process and the user's legal rights, with a true reason (consumables, one-shot items). Never write "non-refundable" or "all sales final" on a store surface (C§5).
  - implied / performance: only if the app moves or earns money for the user AND you bill on the web or your own payment flow.
- Form: "If you [conditions] and don't get [X] by [Y], we [Z]."
- **Per-plan payout table:** plan x platform > Z. Rails:

| Platform | Z options |
|---|---|
| iOS | Renewal-date extension (immediate, up to 90 days, two per 365 days; only active subscriptions with a paid period, not in a free trial or offer period, billing retry or after expiry). Otherwise a free offer code or promotional offer on the same product: it starts at the next renewal and the user must redeem it. Open Apple's refund sheet. Never promise money back. |
| Google Play | Full or partial refund; free time via `subscriptionsv2.defer` |
| Web checkout | Anything, including a refund. You are merchant of record. |

  - Free time for an active auto-renewer must move store billing (the rails above). A RevenueCat promotional entitlement leaves billing running; use it only for lapsed or web subscribers. On an annual plan, free months start at the next renewal: say "your free months start at your next renewal date".
  - Plans with no payable Z (an iOS lifetime or non-consumable) are excluded, and the terms say "subscriptions only". The badge states the smallest payout on any plan shown, or follows the selected plan. Never one figure some plans don't get.
- **Cost:** size Z per plan so claim cost stays below ~10% of that plan's LTGP; for refund-based guarantees use the break-even (1 + lift)(1 - r_new) = (1 - r_old), r_old from C§14 [B] with no history (F§17.2).
- **Claim runbook (required):** where eligibility is computed, the claim path (in-app button to a prefilled email or form carrying the app user ID), the verification source, the payout call and credentials, turnaround, expected claims a month and minutes each (F§17.2).
- Prefer a service guarantee ("Pro free until you hit X"). Give it a vivid name in the brand voice.
- Badge may appear on the paywall, onboarding plan screen, ads, promotional text and website; never in the store name, subtitle, screenshots or previews (Apple 2.3.7).
- Stack: trial + reminder, then the conditional promise, then the price lock.

**8e Naming (MAGIC):** Magnetic reason, Avatar, Goal, Interval, Container.
- Use 3-5 parts. Write 10 variants and mark rhyme or alliteration. Choose 1 control and 2 challengers.
- Interval: prefer process intervals ("7 minutes a day", "30-day sprint"). An unquantified milestone with a duration ("your first 7-day streak") is fine where the platform allows. Never pair a quantified result (money, weight, score gain, IQ) with a deadline.
- Name every plan, bundle and bonus, each with a plain descriptor.
- If a brand voice defines registers, tag each name with where it may appear (in-app vs ads/store/social); the in-app paywall stays in the in-app register.
- Mark whether each name survives translation; otherwise give a per-locale rule (native descriptive name).
- The store title stays brand + keyword. New idea: propose 3 brand names (30 characters or fewer with a keyword; flag trademark and store-search checks), pick one [A], and define the brand voice in one line.

Writes §8.

## Step 9: Assemble

1. **One-sentence offer:** "[Name]: [avatar] get [goal] in [interval/effort], with [stack], [guarantee], for [price]." Would the avatar feel stupid saying no? Write the top remaining reason to say no and its answer.
2. **Paywall per placement** (onboarding / contextual feature-gate / milestone / settings). For each: plans shown (Step 7.5), lead element, source of the personal line, trial CTA or not, guarantee badge text per plan shown, urgency eligibility. Element order: headline = offer name + outcome; personal line; 3-5 named bundles plus an expandable "everything included"; proof row (real rating, real outcome stat); plans (hero pre-selected, billed price largest, per-period small); guarantee badge with one line of terms; urgency line only if real and dated; CTA with trial length, charge date, amount, auto-renew and how to cancel; restore, Terms, Privacy, and a visible dismiss if freemium (C§2). Every bonus, line and badge maps to a §14 row; nothing shows before its row ships (Apple 2.1).
3. **Onboarding fast-win plan:** goal > obstacles > baseline / first win > personalised plan reveal > commitment (pick a time) > permission explainer (opt-in) > paywall. Multi-user: the account step and invite go after the first win, before or after the paywall; test the placement. State the first-win target in seconds. Every answer must visibly change something later. Read the store age signal and handle pending, denied or revoked consent (C§10); cross-platform frameworks need a native bridge, counted in §14.
4. **Where the ask happens.** Recommend one and state the trade-off with C§14 numbers (conversion, retention, refunds):
   - Paid acquisition needing fast payback: an onboarding paywall (hard, or soft with a trial) after the first win.
   - Organic or ratings-driven growth: a soft onboarding paywall plus contextual and milestone paywalls; delay the big asks (lifetime, top tier) until the user has invested.
5. **Post-purchase wow** in the first 60 seconds: reveal the bonuses; show the first Pro benefit already built from the user's data; plan a day-2 progress message.
6. **Decline flow:** one screen adding value aimed at the stated objection, not a discount. Cap re-asks (e.g. after value moments on day 3 and day 7).
7. **Review prompt:** native API only, on a behavioural milestone (sessions completed, goal reached, personal best). Never on the value of any in-app rating, mood or satisfaction score.

Writes §9.

## Step 10: Test and rotation plan (Read F§1.5, F§13.7, F§17.3)

- **New idea: validate before building:** a landing page with the offer name and price, a waitlist, ad CTR on 3 names, and a 5-10 user concierge pilot with an explicit gate metric.
- **Traffic check:** n per arm ≈ 16 x p(1 - p) / Δ². Example: p = 3%, Δ = 3 points (a 2x lift) needs about 520 paywall views per arm. If the detectable lift is above ~50% relative, test only big swings (2x price, trial vs none, hard vs soft, new name or niche) or a dated before/after with a holdout.
- **First 3 tests, in order:** hypothesis | variant | primary metric | sample and duration | ship rule.
- **Rotation order when response fades** (light to heavy): creative > copy > headline / offer name > goal angle > seasonal reason > duration > enhancer > monetisation model. Exhaust lighter layers first; mark which change remotely without a release.
- **Metrics**, each with a target and kill criterion: install-to-trial, trial-to-paid, refund rate, D1/D7/D30 retention, ARPU / revenue per install (D14, D35), LTGP, payback days; multi-user: invite-sent rate and second-user join within 7 days (north star). Decide on revenue per install, not trial starts. Kill a variant that loses on revenue per install after the planned sample, or whose refund rate exceeds 2x baseline.
- **Offer log:** tag events with `offer_id`; one-line post-mortem per losing variant.

Writes §10.

## Step 11: Scorecard, verdict and ship plan

- **§11:** before/after table (4 market tests, 4 value drivers, enhancers present, value-to-price ratio, LTGP per plan); the "feel stupid saying no" test (passes only if every top-5 §4 objection is answered in onboarding or on the paywall and the risk block covers fear #1); top 3 risks (market, compliance, economics, execution, user safety), each with a mitigation. Verdict: existing app SHIP / SHIP AFTER FIXES / RETHINK MARKET; new idea BUILD / BUILD AFTER VALIDATION / RETHINK MARKET.
- **§12:** the three-part offer before vs after (what they get, how they pay, terms, where they are asked).
- **§13 checklist:** disclosures; claims and labelled estimates; kids/teens and age signals; sensitive data (C§16, including whether the developer account must be an organisation); guarantee payable per plan and badge text matching the payout table; scarcity/urgency honesty; privacy label and policy changes from new data (onboarding answers to analytics, claim emails); misuse and safe exit (leave a shared account, split or delete data).
- **§14 ship plan:** table: change | where (code file / ASC / Play Console / RevenueCat / remote config / web) | needs release? | needs review? | locales touched | effort days | wave. Wave 0 = §0 audit fixes. Then store setup (product IDs, prices, trials, intro offers, offer codes, in-app events with dates), RevenueCat Offerings and entitlements, and an event spec (event | properties incl. offer_id, placement, variant | source: app or RevenueCat integration).

Writes §11-§14 and Appendix C (copy deck: every new user-facing string in English, plus a translation budget line per locale).

## Output

- **Path:** `offer/grand-slam-offer.md` in this app's project root (`mkdir -p offer`). New idea or unrelated working directory: `./<app-slug>-grand-slam-offer.md`. Never write into, or rename, another app's offer file.
- If the file exists, rename the old one to `offer/grand-slam-offer.<YYYY-MM-DD>.md` first.
- Use these exact headings. Fill every one, or write "n/a: reason".

```markdown
# <App name>: Grand Slam Offer
Generated by app-offer on <YYYY-MM-DD>. [A] = assumption, [B] = benchmark stand-in. Constraints as of <C§ date>; re-verify before shipping.

## Decisions (one screen: niche, price grid, guarantee, offer name, paywall placement, top 3 tests, next 5 actions)
## 0. Inputs, assumptions, prior decisions, compliance audit
## 1. Market
### 1.1 Four tests (score table per candidate) and H/W/R
### 1.2 Verdict and market / offer / persuasion rating
### 1.3 Niche ladder, avatar, not-for, harm, positioning sentence, TAM
## 2. Commodity check
## 3. Value equation audit
## 4. Problem inventory (top 25)
## 5. Solutions and delivery vehicles
## 6. Trimmed stack and bundles
## 7. Pricing and tiers
### 7.1 Price grid
### 7.2 Unit economics (LTGP, max CAC, day-30 proceeds, day-75 cash, first $100k)
### 7.3 Growth levers, regional pricing, price-rise protocol
## 8. Enhancers
### 8a Scarcity
### 8b Urgency
### 8c Bonuses
### 8d Guarantee (per-plan payout table, cost, claim runbook)
### 8e Naming
## 9. The offer
### 9.1 One sentence
### 9.2 Paywall per placement
### 9.3 Onboarding fast-win plan and where the ask happens
### 9.4 Post-purchase wow, decline flow, review prompt
## 10. Test and rotation plan
## 11. Scorecard and verdict
## 12. Before / after offer (n/a: new idea)
## 13. Compliance checklist
## 14. Ship plan (changes table, store and RevenueCat setup, event spec)
## Appendix A. Alternatives considered
## Appendix B. Sources and data used (URLs, dates, To verify before pricing)
## Appendix C. Copy deck
## Appendix D. Full problem inventory and how-to lines
```

## Final reply (10 lines max)

1. The one-sentence offer.
2. The price grid, one line per plan.
3. The guarantee: name and terms.
4. The verdict and the top risk.
5. The file path.
