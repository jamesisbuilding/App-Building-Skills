# app-offer frameworks

Every framework in *$100M Offers* (Hormozi) is distilled here and translated for apps. Chapters are cited as "Ch. n". Everything is paraphrased. The book's arithmetic is reproduced as the book gives it, and corrected where it is wrong. Store rules referenced here are in `app-store-constraints.md` (C§). F§16 lists the ideas judged not applicable to apps, with reasons. F§17 holds the runner formulas that SKILL.md points to.

Book chapter map:
- Ch. 1 How we got here
- Ch. 2 Grand Slam Offer
- Ch. 3 Pricing: the commodity problem
- Ch. 4 Finding the right market
- Ch. 5 Charge what it's worth
- Ch. 6 The value equation
- Ch. 7 Free goodwill
- Ch. 8 The thought process (divergent thinking)
- Ch. 9 Creating your offer I: problems and solutions
- Ch. 10 Creating your offer II: trim and stack
- Ch. 11 Enhancing the offer (overview)
- Ch. 12 Scarcity
- Ch. 13 Urgency
- Ch. 14 Bonuses
- Ch. 15 Guarantees
- Ch. 16 Naming
- Ch. 17 Your first $100,000 / closing

What changes for every framework below:
- The paywall and onboarding replace the sales call.
- The store controls refunds, payouts and how prices are displayed.
- Marginal cost is close to zero, except for AI inference, human time and third-party data or API fees.
- The store takes 15-30%.
- App prices are anchored far lower than service prices.

---

## F§1 Foundations (Ch. 1-3)

### 1.1 Asymmetric bets
- **Book:** Business payoffs have no cap. A 10% chance of a 100x return is worth taking every time, even though you'll be wrong 9 times out of 10. One grand slam offer can be enough.
- **App:** Treat offer design as a portfolio of cheap experiments: remote paywalls, RevenueCat Offerings, custom product pages. App revenue follows a power law (the top 10% of apps take about 94.5%; C§14), so one winner pays for the losers.
- **Do:** Test genuinely different offers (outcome program vs "Pro", 2x price, trial vs none, new niche), not tweaks.
- **Breaks:** Low traffic can't detect small lifts (F§17.3). New IAP products and metadata need review.

### 1.2 What an offer is, and the offer ladder
- **Book:** An offer is three things: what you deliver, how you take payment, and the terms. The quality ladder runs: no offer (no business), bad (losing money), decent (stagnant), good (some profit), grand slam (outsized profit).
- **App:** The offer is:
  - the free vs paid split
  - the plan lineup and billing cadence
  - the trial and intro terms
  - cancel and refund terms
  - Family Sharing or household seats
  - the purchase route (store one-tap or web)
  - the promise made in onboarding

  Payment friction is part of the offer.
- **Breaks:** Stores dictate auto-renew, cancellation through OS settings and Apple's refunds. You can't sell "pay after results" inside IAP.

### 1.3 Make an offer so good people feel stupid saying no
- **Book:** A mentor's lesson: you don't need to be a great seller if the offer makes yes the obvious answer.
- **App:** The paywall is the closer and gets a few seconds. To make yes obvious, combine an outcome promise, a personalised plan, low risk (trial plus reminder) and a clear price per outcome.
- **Rubric:** Would a sceptic feel foolish declining? Name the top reason to say no, and check the offer neutralises it.
- **Breaks:** It must be irresistible through value, never through tricks: hidden close buttons, trial toggles that switch plans, fake countdowns (C§8).

### 1.4 The grand slam offer is a learnable skill
- **Book:** Pricing + value + guarantee + naming, combined well, reliably turn ad spend into profit. The author reports a 36:1 lifetime return; that is his track record, not a target.
- **App:** Measure your "batting average" as cohort ROAS and payback days per offer variant. Use RevenueCat/Mixpanel cohorts, not click attribution, which ATT has made noisy.

### 1.5 Diagnose, iterate, depersonalise (about 100 offers)
- **Book:** Understanding why you failed is worth more than not knowing why you won. Try many offers. A failed offer is a bad offer, not a bad you.
- **App:** Instrument store page, onboarding completion, paywall view, trial start, trial-to-paid and renewal. Tag every event with `offer_id`. Keep an offer log of hypothesis, result and one-line post-mortem.
- **Breaks:** Trial-to-paid takes days and renewals take weeks, and 100 offers isn't realistic at indie volume. Rank tests by expected impact.

### 1.6 Commodity vs category of one (Ch. 3)
- **Book:** A commodity is available from many sellers, so people buy on price and margins sink to survival level. A differentiated offer has no comparison, so it is bought on value.
- **App:** Store search lines up about 20 lookalike apps with ratings and prices. Free substitutes (web tools, YouTube, ChatGPT, the OS) set a $0 reference price.
- **Test:** Shown next to 5 competitors, what makes this impossible to compare? Would users call it "basically X"?
- **Fix:** A named method, an avatar, an outcome with an interval, and named systems instead of a feature grid.

### 1.7 The grand slam definition: five parts
- **Book:** An attractive promotion, a value proposition nobody can match, a premium price, a strong guarantee, and a money model that gets you paid to acquire customers.
- **App checklist:**
  - Promotion: hook, launch, challenge, season.
  - Value proposition: outcome plus stack.
  - Premium price.
  - Guarantee, within store limits (C§5).
  - Money model: upfront plans, web checkout where allowed, upsells.

### 1.8 Same delivery, different offer
- **Book:** With identical delivery, a better offer makes the business look like a different product and resets the buyer's value meter. Let the offer do the explaining.
- **App:** Repackage the existing features as an outcome program without writing new code. Store screenshot 1 and the paywall headline must make the difference obvious in about 2 seconds. Store metadata must stay accurate (Apple 2.3).

### 1.9 The two root problems and the discount spiral
- **Book:** Almost every problem is too few customers or too little profit. Cutting prices to win customers kills the margin that pays for acquisition. Copying the models of well-funded firms buys you a job.
- **App:** Indie developers copy VC-funded freemium economics (giant free tier, ads, cheap monthly plans). Low LTV means you can't outbid anyone on ads.
- **Ask:** Whose pricing am I copying, and are they profitable or just funded? What maximum CAC does my LTGP support?

### 1.10 Grow or die; the three (really two) growth levers
- **Book:** Standing still means falling behind: about 9% a year just matches the market. Growth comes from more customers, a higher value per purchase, or more purchases. Ceiling = new customers per month x LTV. For example, 10 a month x $1,000 caps out at $10k a month.
- **App:** Steady-state revenue is roughly new payers per month x lifetime revenue per payer. The levers are:
  - conversion
  - revenue per payer (price, plan mix, upsell to annual or lifetime, top tier)
  - number of purchases (retention, add-ons, packs, family or household plans)
- **Breaks:** A lifetime plan caps purchases at one unless there is something else to buy. With churn, even holding revenue flat needs constant acquisition.

### 1.11 Gross profit and LTV (lifetime gross profit)
- **Book:** Gross profit is revenue minus the direct cost of serving one more customer. LTV is gross profit per purchase x number of purchases. Example: $1,000 x 90% x 5 months = $4,500.
- **App formula:** LTGP = price x (1 - store fee) x (1 - VAT share) x average paid periods - variable cost (inference, human time, SMS, third-party data or API fees, revenue-share tools). Estimate paid periods with F§17.1.
  - Non-AI apps run at about 80-85% margin.
  - AI-heavy or data-heavy apps (bank aggregation, OCR) can fall to 30-60%, or go negative for power users. Model the 95th-percentile user; cap usage or price it separately.
- **Contrasting examples at a 15% fee, before VAT** [A]: weekly $2.99 x 0.85 x 10 paid weeks ≈ $25; annual $39.99 x 0.85 x 1.4 paid years ≈ $47.60; lifetime $89.99 x 0.85 ≈ $76.50 once (Google one-time purchases may carry a different fee, C§1).
- **Breaks:** Dashboards show revenue, not LTGP, and early cohorts underestimate the long tail.

### 1.12 Money model: collect cash upfront
- **Book:** The author's low point was a frozen processor balance and a drained account. What saved him was an offer that collected all the cash upfront. If cash collected early exceeds CAC, cash no longer limits growth.
- **App:**
  - Make an upfront plan (3-month, annual or lifetime) the default.
  - Track proceeds earned by day 30 against CAC, and cash actually received by about day 75 for runway: Apple pays about 45 days after the fiscal month, Google monthly, and trials delay the first charge.
  - Diversify, because web processors can freeze funds too.
- **Breaks:** Trials delay cash. Apple can claw money back through refunds. Lifetime trades renewals for cash today.

### 1.13 Better offers multiply through the funnel
- **Book:** A better offer lifts response, conversion and price at the same cost per eyeball. In the agency example (the book says the figures are rounded for illustration):
  - Old model: $1,000 down plus a $1,000/month retainer. $10k of ad spend collects $5k upfront (0.5:1) and breaks even in month 2.
  - New model: a one-time fee, lead generation the client pays for only when people show up, a "20 people in month 1 or next month free" guarantee, and a large playbook bonus.
  - The claimed result is 2.5x response x 2.5x close x 4x price, giving 22.4x more upfront cash: $112k under the new model against the old model's $5k. The rounded factors multiply to 25x; the new model's own ROAS is 11.2:1. Use the method, not the figure.
- **App:** Build an old-vs-new table covering spend, CPI, trial start, trial-to-paid, plan-mix price, and day-30 proceeds vs CAC. Then name the next bottleneck: creative volume, AI cost, support load.

### 1.14 Changing the offer is the cheapest lever
- **Book:** A new offer is easier to implement than management or culture change.
- **App:** Plan mix, default plan, trial, program name and bonuses can ship remotely in a day. New product IDs and price rises for existing subscribers have rules (C§4).

### 1.15 Give free value, then monetise the people who prove themselves
- **Book:** The author gives his material away free, then works with people who have already executed. Proof lowers risk for both sides.
- **App:** The free core loop and free social content are the trust engine. Show the upgrade to users who have shown the behaviour that predicts success, such as a streak or a measured gain. The free tier must lead into the paid offer, not replace it.

### 1.16 Most buyers never use what they buy
- **Book:** Most people never get far into what they buy, so finishers are rare. Show that the bigger payoff is still ahead.
- **App:** Activation is the real battle. "Zombie" subscribers turn into refunds and 1-star reviews (Apple 5.6.4). Show future unlocks on a progress map.

### 1.17 Treat this as a reusable tool
- **Book:** Look things up instead of memorising them; repeat the frameworks.
- **App:** Re-run app-offer each quarter with fresh RevenueCat and Mixpanel numbers and the experiment log.

---

## F§2 Market (Ch. 4)

### 2.1 Starving crowd
- **Book:** A hot-dog stand's best advantage is a hungry crowd. With enough demand, a mediocre operator still makes money (the COVID toilet-paper example).
- **App:** Look for existing intent and demand surges: exam seasons, platform shifts, viral formats, rising keyword popularity, AI waves.
- **Breaks:** Surges attract clones within days. Turn surge demand into a durable brand quickly.

### 2.2 Shrinking markets sink good businesses
- **Book:** A friend with a great product, a zero-risk offer and a gifted seller still failed because newspapers were shrinking about 25% a year. The same founder then made millions a month in a growing market.
- **App:** Check category trends and the risk of being absorbed by an OS feature or a free AI assistant ("Sherlocking"). Code and skills transfer when you pivot. Reviews and keyword history don't.

### 2.3 Channel demand, don't create it
- **Book:** You can't create desire, only channel it. Serve people who can pay what you're worth.
- **App:** Build for intent you can see: search terms, competitors' 1-3 star reviews, Reddit requests. Don't pick an audience because you like them if they can't pay.

### 2.4 The normal market: health, wealth, relationships
- **Book:** These three needs never go away. A "normal" market, growing about as fast as the economy with unmet needs, is enough.
- **App:** Map the app to H, W or R. The framing changes the pain and the price ceiling. Examples:
  - Mental maths as health (health framing needs substantiation, C§7; prefer measured skill outcomes), wealth (pass a numerical interview) or relationships (help with your kid's homework).
  - A couples budgeting app as relationships (fewer money arguments) or wealth (a shared savings goal); money outcomes are claims (C§7).
  - Pure entertainment sells fun or status, so pain-based pricing fits less well.

### 2.5 The four market tests (rubric in SKILL step 1)
1. **Pain.** People must need it, not just want it, and the size of the pain sets the price. The pain is the pitch: describe it so precisely that the buyer feels understood.
   - App: onboarding asks about the pain and reflects it back in the user's words.
   - Ad platforms forbid copy that asserts personal attributes ("Are you bad at maths?").
2. **Purchasing power.** The resume-fixer example: lots of pain, but the users were unemployed.
   - App: separate the payer from the user (parent vs child, employer vs employee, one partner vs the household). Check user-geography LTV (C§14). Localise prices.
3. **Easy to target.** A perfect market you can't reach is worthless.
   - App: is there a keyword cluster, a community, creators, and a distinct custom product page? Since ATT, the ad's hook does the targeting.
4. **Growing.** A tailwind speeds everything up; a headwind slows everything down.
   - App: category download and revenue trends, plus macro trends (ageing, AI adoption).

### 2.6 Pick a sub-group
- **Book:** Inside H/W/R, find the sub-group that is in more pain, richer, easier to find and growing. The example is later-life relationships over college dating: more people now turn 65 each year than turn 20.
- **App:** Score 2-5 candidate segments on the four tests before building tracks. Check the segment is smartphone-native and buys through app stores. The SKILL step 1 verdict judges the market as stated; sub-groups only matter if it falls short.

### 2.7 Market > offer > persuasion
- **Book:** Rate each as great, normal or bad.
  - A great factor higher up overpowers anything below it.
  - Normal passes the decision down to the next factor.
  - Bad stops everything unless a great factor above cancels it.
  - Normal market + grand slam offer is the realistic path. Normal + normal needs exceptional persuasion, which is the hardest route.
- **App:** Fix the segment first, then packaging, plans, trial and guarantee, then persuasion: paywall animation, ads, screenshots. This is why SKILL step 1 allows "GO (normal market)".

### 2.8 The niche slap: commit
- **Book:** Founders try one offer, don't hit big, and switch markets. Any normal market works, but not two at once, and switching resets your learning to zero.
- **App:** Iterate offers within one segment. Parallel segment tests through custom product pages or onboarding branches are fine early on. Commit once one shows a signal.

### 2.9 Riches in niches, and when to broaden
- **Book:** Under about $10M a year, narrower is easier and more profitable (only about 0.4% of businesses reach $10M). Beyond that, total addressable market decides, and you move up-market, down-market or to an adjacent market. The counterweight: many companies passed $30M a year in a single niche, and founders at $1-3M who think they have hit the ceiling usually just need to get better.
- **App:** Low app prices mean the TAM limit can arrive earlier. Compute it, don't assume it: reachable payers x LTGP. Broaden only when the computed ceiling, not a plateau, is below the goal; then plan the adjacent niche that reuses about 90% of the product.

### 2.10 One avatar, and who to turn away
- **Book:** Gym Launch defined a micro-gym owner precisely and turned everyone else away.
- **App:** Write the avatar with 4 qualifiers and an explicit not-for list. You can't block downloads, so set expectations on the store page and in onboarding. Add who could be harmed by the product or its misuse (a controlling partner, a minor, a vulnerable user) and make the risky offer elements opt-in.

### 2.11 The niche price ladder and the positioning formula
- **Book:** The same time-management course is worth about $19 generic, $99 for salespeople, $499 for B2B outbound reps, and about $1,997 for B2B outbound reps in a specific trade. Positioning formula: solve [problem] for [specific person] in a [unique] way that removes their deepest fear.
- **App:** One engine with niche packaging: tracks, vocabulary, custom product pages, and offerings chosen by the onboarding answer. Expect a 2-5x premium, not 100x. Use one app with tracks rather than clones, because clones fall under Apple 4.3 spam rules.

### 2.12 Switching trigger
- **Book:** People change when staying the same hurts more than changing.
- **App:** Aim hooks and creative at trigger moments (exam announcements, interview season, moving in together, tax day). Make switching cost tiny: one-tap start, no account before value.

---

## F§3 Pricing (Ch. 5, plus the start of Ch. 6, Ch. 11)

### 3.1 Charge what you can say with a straight face; price far above cost
- **Book:**
  - Premium pricing is the first step. Charge well above what delivery costs you (think up to 100x), but never more than the thing is worth.
  - A photography business went from a $300 to a $1,500 ticket. It spent less time per customer, and profit rose about 38x.
- **App:** Price from the outcome and the user's next-best alternative (a tutor, a course, a counsellor, hours of their time), not from "it's only an app". Run the 100x test against variable cost, not zero. Most indie apps never test 2x their current price.

### 3.2 Frame the price against the outcome (the dad conversation)
- **Book:** A $42k fee looked like a scam until it was set beside a $239k gain, the effort it took and the time to result.
- **App:** Put the outcome, the time cost per cycle, the time to result and the risk reversal next to the price. Per-day framing is allowed, but the billed amount stays most prominent. Outcome claims must be substantiated.

### 3.3 People buy deals: the value-price gap
- **Book:** People buy when perceived value exceeds price and stop the moment it doesn't. Raise value first, then price. Target value at about 10x price.
- **App:** Every renewal is a new purchase decision, and a weekly plan re-tests value 52 times a year. Churn means value fell below price for that cohort. Show a value recap before renewal. Consumer apps under ~$200/yr rarely reach an honest 10x; report the real ratio and never pad it (SKILL step 7.3).

### 3.4 Don't compete on price; avoid the copy-the-market trap
- **Book:**
  - Price can fall to zero but has no ceiling.
  - Only compete on price if your costs are a tenth of your rivals'.
  - Dan Kennedy: there's no strategic advantage in being the second-cheapest, but there is one in being the most expensive.
  - Averaging competitors and undercutting them imports their broke economics. The bottom 10-20% wash out each cycle.
- **App:** Default to the top quartile or the top of the category, with a stack that looks visibly different; any lower position needs a written reason (F§16). The cost exception is real when AI replaces a human tutor or coach (a 10x cost advantage). Otherwise check whether the competitors you copy are actually profitable (Appfigures or Sensor Tower estimates).

### 3.5 Maximise money, not customers; the virtuous cycle of price
- **Book:** Low prices bring low commitment, low perceived value, poor results, the worst customers and no margin. High prices reverse each of those, and the margin pays for systems, talent and growth. Premium pricing is also the moral choice, because it funds better service.
- **App:**
  - Optimise revenue or LTGP per install, not conversion rate.
  - Compare support tickets, reviews and retention across plans.
  - Spend the extra margin on content, creators and paid acquisition.
- **Breaks:** Store ranking rewards downloads, so a free tier often stays wide open.

### 3.6 Price raises perceived value (the wine study) and adds allure
- **Book:** Tasters rated the same wine higher when it carried a higher price. Price far enough above the market and buyers assume it's a different thing altogether.
- **App:** A visible premium tier or lifetime anchor makes the core plan look reasonable and signals seriousness. $0.99 signals a toy. Extreme prices in the IAP list can still hurt install conversion.

### 3.7 Price as a commitment device
- **Book:** If results depend on the customer's effort, the price should sting a little, because people who pay more pay more attention.
- **App:** This fits habit and skill apps. Use upfront 3-month or annual plans plus commitment rituals (accepting the plan, picking a training time). A small weekly price barely stings. Lifetime removes the recurring reminder.

### 3.8 Conviction comes from proof
- **Book:** Survey results drove his conviction: 158 gyms after 11 months showed revenue up, profit about 3.1x and churn down from 10.7% to 6.8%. You can only ask big prices if you know the customer will succeed.
- **App:**
  - Measure outcomes in the app.
  - Survey users around day 30.
  - Publish honest aggregate proof on the paywall, store page and social.
  - Small samples mislead. Cognitive claims draw scrutiny (C§7).

### 3.9 Productise: done-for-you to done-with-you
- **Book:** Flying to gyms for 21-day relaunches capped capacity at about 8 a month. Remote coaching while the owner did the work produced similar results and scaled to thousands.
- **App:** Run manual pilots with a few users (hand-written tips, reviews), learn what works, then automate it as a feature or AI. This gives three natural tiers: DIY app, DWY plan or AI coach, and a scarce DFY human tier (licensed partner where a credential is needed).

### 3.10 Premium anchor, then upsell to continuity
- **Book:** Gym Launch wanted to be the premium price leader and entered at $16k for 16 weeks: 3x the top competitor and 32x the cheapest. It then upsold 35% of buyers into $42k a year.
- **App:**
  - Map the category's lowest, typical and highest prices and choose your position deliberately (default: top quartile or top, F§3.4).
  - Pair a front-end program (a 30-day bootcamp) with a continuity offer (annual or lifetime) shown at the moment of success.
  - 35% is a high-touch service benchmark, not an app norm.

### 3.11 Profit is oxygen
- **Book:** Almost every business needs to raise prices, not lower them. Margin funds bold bets.
- **App:** Assume the price is too low until proven otherwise. Raise value, then price. Test on new users first and grandfather existing ones (C§4).

### 3.12 Pricing-model changes are the highest-leverage fix
- **Book (Ch. 12 aside):** An hour spent changing a pricing model added millions in profit.
- **App:** Before building features, audit:
  - trial length and type
  - the default plan
  - adding lifetime
  - hard vs soft paywall
  - paywall placement
  - which features sit behind the gate
  - regional prices
  - annual-first presentation
  - per-user vs household pricing (multi-user apps)

### 3.13 Demand is fractal 80/20: price the top of the pyramid
- **Book (Ch. 11):** Ten seats at $500 earn $5k; two one-on-one slots at $5k earn $10k. About a fifth of prospects will pay 5x or more.
- **App:** Software doesn't force a choice. Sell volume at the base price and add a top tier at 5-10x annualised Pro for the top fifth. Most indie apps have one price point and leave the top untouched.

---

## F§4 The value equation (Ch. 6)

### 4.1 The formula
Value = (Dream outcome x Perceived likelihood of achievement) / (Perceived time delay x Perceived effort and sacrifice).

Each driver answers one of a sceptic's questions:
- Will I get what I want?
- How do I know it will work?
- How long will it take?
- What will it cost me besides money?

**App:** Every paywall, onboarding flow and screenshot set needs at least one element per driver:
- an outcome headline
- proof or personalisation
- time to first result
- an effort statement

### 4.2 Compete on the bottom of the equation
- **Book:** Beginners make bigger promises, which is easy to copy. Winners make things instant and effortless (one-click buying, streaming). As time and effort approach zero, value approaches infinity.
- **App:** Value before signup, a one-tap start, widgets, automatic input, offline use, no setup. When Pro unlocks, show a benefit already built for the user, not an empty feature. Ask for permissions after value has been felt.

### 4.3 Perception is reality
- **Book:** London Underground riders became much happier when countdown boards showed the next train. Faster trains would have cost billions; the boards cost far less.
- **App:**
  - Skill graphs
  - "X days to your goal"
  - "12% faster than last week"
  - Session timers
  - A plan-building screen
  - A cheap UI change often beats a backend project.
- **Breaks:** Fake progress or fake "analysing" delays count as deception (C§8).

### 4.4 Psychological fixes beat logical ones
- **Book (crediting Rory Sutherland):**
  - Mirrors by lifts instead of faster lifts.
  - Make the journey pleasant instead of shorter.
  - Make fewer and charge more instead of cutting the price.
- **App:**
  - Rename, reorder, gamify, or make waits entertaining (mascot lines).
  - Streak freezes reduce the fear of losing a streak.
  - Use honest limited runs instead of discounts.
- **Breaks:** Retention curves expose a broken core loop, whatever the framing.

### 4.5 Dream outcome is status
- **Book:** Deep desires (beauty, respect, power, love, status) stay the same; many vehicles serve each one. Status is relative to the peer group, as in the minivan example: a Lamborghini would lower a mother's standing among other parents.
- **App:** Find the status outcome and the peer group behind the function. Being the quickest at mental maths in the room beats "arithmetic practice"; never claim work or school performance gains without evidence (C§7). For couples or families, the "peer group" may be the partner or household: the scene is calm, fairness or a shared win. Ask the "why" in onboarding and echo it in the paywall headline.
- **Minivan test:** would visibly using this app raise or lower standing in the user's group?

### 4.6 Describe benefits as other people see them
- **Book:** The example is a golf club that adds yardage, described as friends' reactions.
- **App:** Write copy that describes the social scene, then make the scene real with share cards, duels and leaderboards. Comparison claims on share cards must be true.

### 4.7 When the desire is the same, the other three drivers decide
- **Book:** That is why one beauty solution costs $50k and another $5.
- **App:** In crowded categories, the headline outcomes cancel out. Win clearly on likelihood, time or effort, and show it within about 3 seconds of the store page.

### 4.8 Perceived likelihood: people pay for certainty
- **Book:** You would pay more to be a surgeon's 10,000th patient than their first. Proof, track record, what you include and what you leave out, and guarantees all raise certainty.
- **App proof stack:**
  - rating and count
  - matched testimonials (with permission, and any incentive disclosed; C§7)
  - measured outcome stats
  - credibility of the method
  - a personalised plan
  - a progress forecast
- New apps borrow certainty: the founder story, research behind the method, beta cohort results, the trial.
- **Breaks:** Apple owns iOS refunds. Google Play and web checkout allow developer refunds (C§5).

### 4.9 Time delay: buy the dream, stay for the benefits along the way
- **Book:** People buy the long-term outcome and stay for short-term wins: energy and new friends on the way to a fitness goal. Put a big emotional win as close to purchase as possible. Long waits are part of why surgery sells for many times the price of a boot camp.
- **App:** The trial or first billing period is the deadline. Engineer a felt, measured win before the trial ends or the first renewal. Map milestones at the app's cadence (for a daily app: day 1, 3, 7 and 30; for a weekly app: first session, week 1, month 1).

### 4.10 Fast wins, and fast beats free
- **Book:**
  - Always build in immediate wins so customers know they chose right.
  - The only thing that beats free is fast: skip-the-queue services, overnight delivery, ride-hailing.
- **App:**
  - Design the 60 seconds after purchase and the second-session return.
  - Sell Pro as the fastest route to the outcome, not as "more features".
- **Breaks:** Deliberately slowing the free tier (energy timers, forced ads) reads as punishment.

### 4.11 Effort and sacrifice
- **Book:** Count every non-price cost: lost hours, foods given up, embarrassment, injury risk, fear of relapse. Fitness sells for a fraction of what surgery does because surgery removes effort. Done-for-you costs more than do-it-yourself.
- **App:** List 10 sacrifices:
  - minutes
  - remembering
  - setup
  - account
  - data entry
  - permissions
  - notification noise
  - being bad in front of others
  - streak anxiety
  - privacy

  Remove or reframe each one. In apps, DFY = automation or AI, DWY = guided plans, DIY = tools.
- **Calibrating the SKILL step 3 anchors by app type** (what a 5 looks like):

| App type | Effort 5 | Time 5 |
|---|---|---|
| Daily habit or skill game | One tap from a widget, no account, offline, a short fixed session | First win in under 60 seconds |
| Utility (scan, convert, track) | Works on the first share or scan, no setup | First result in under 30 seconds |
| Multi-user or finance (couples budget, family planner) | A first insight from one manual entry or sample data before any account or bank link; partner joins via one link | First insight in session 1; the real value lands after the first weekly cycle |

### 4.12 Score vehicles 0 / 0.5 / 1
- **Book:**
  - Meditation scores about 1.5/4 on the drivers and the anxiety pill 4/4. A 1 means the driver favours the buyer: for time and effort, fast and easy.
  - Supplements (about $123B) beat gyms (about $62B) because they are faster and easier.
  - Work with human nature: be rich rather than right.
- **App:** Score the app and every substitute (SKILL step 2). Ask which product is the "pill" of the category and how the app can work more like it.

### 4.13 Sell what they want, deliver what they need
- **App:** Wrap deliberate practice in a game, status, speed or fun. Market the want and build the need into the loop. Avoid dark patterns.

### 4.14 A commodity can't be rescued by a lower price or a free start (Ch. 9 opener)
- **Book:** A $99 boot camp lost to a $29 gym even with a free start, because people still judged the ongoing price and feared they wouldn't stick with it.
- **App:** A free trial doesn't fix a commodity offer. A low trial-start rate signals a weak offer, not a high price. Address the fear of not sticking with it.

---

## F§5 Free goodwill (Ch. 7)

- **Book:** Right after delivering value, ask for a review. Frame it as helping someone like the reader's earlier self, and stress that it is free and takes under a minute. People link the value of something good to the person who introduced it.
- **App:** Trigger the native rating prompt at a behavioural peak (a milestone, a goal reached, a personal best), never cold, never from a button, and never on the value of an in-app mood or satisfaction score (that is sentiment gating). Frame sharing and referral as giving a friend something useful.
- **Rules (C§7):** Apple allows 3 prompts per 365 days and no custom prompts. Google forbids pre-questions. Incentivised reviews and review gating are banned; the FTC rule adds civil penalties.

---

## F§6 Divergent thinking (Ch. 8)

### 6.1 Divergent before convergent
- **Book:** Convergent problems have one answer. The rep-hiring maths: 100 calls / 4 calls per close = 25 closes per rep, so 110 sales needs 5 reps. Offer design is divergent: many answers, and one is far better than the rest.
- **App:** Generate many options per problem before pruning. Then do the convergent funnel maths: subscribers needed > trials needed > installs needed.

### 6.2 The brick exercise
- **Book:** List uses for a brick in 2 minutes, then change its size, material and shape to find many more.
- **App:** Change one attribute at a time:
  - surface: phone, widget, watch, lock screen, web, voice
  - format: game, lesson, challenge, AI chat
  - social size: solo, partner, friend, league
  - session length
  - audience
  - payer: user, partner, parent, employer, school
- **Breaks:** Each surface means native code on two platforms, so generate freely and trim hard.

---

## F§7 Building the offer (Ch. 9-10)

### 7.1 Step 1: dream outcome (sell the destination)
- **Book:** Nobody wants a gym membership; they want weight off by a date. Sell the destination, not the plane.
- **App:** The headline is a specific result and timeframe that the app can measure. Prefer process intervals or unquantified milestones over quantified outcome dates (F§13.3).

### 7.2 Step 2: list every problem, in order
- **Book:** List everything the customer struggles with, in the order they meet it, including what happens just before and after use and what they will need next. Use four belief buckets per core activity:
  - not worth it
  - won't work for me / I won't stick with it / outside factors
  - too hard / I'll be bad at it
  - too slow / too busy

  Four activities x four buckets gives 16 core problems, and with sub-problems about 32-64. More problems means more value you can add.
- **App:** Use the journey in SKILL step 4. Mine your own and competitors' reviews, Reddit, support email, cancellation surveys and drop-off funnels, because no sales call surfaces objections for you.

### 7.3 Step 3: turn problems into "How to..." solutions
- **Book:** Reverse each obstacle into a "how to" line. It will feel repetitive, and that's expected. Missing even one can block the sale. The relationship-course example works the same way.
- **App:** Use the "How to [benefit] even if [objection]" pattern. Spread the lines across paywall bullets (3-5 fit), onboarding reassurance screens, screenshot captions and the FAQ. Copy points to a solution; it is not the solution (F§7.8).

### 7.4 Overdeliver on the first offer
- **Book:** Early on, do things that don't scale. Price high, but make it feel like a steal ("all this for only that?").
- **App:**
  - Personally welcome the first 100 payers.
  - Hand-tune plans.
  - Answer every review.
  - Frame annual against the short plan and lifetime against years of the hero, using accurate numbers and no fake "was" prices.

### 7.5 The sales-to-fulfilment continuum
- **Book:** Delivering more makes selling easier and fulfilment harder. Create demand first, then systematise or add friction. The Gym Launch relaunch (21 days on site, a refundable $500 deposit) gave way to remote teaching: about a third of the revenue per gym, but hundreds of gyms instead of 8. The promise stayed fixed.
- **App:** Launch generous (soft paywall, long trial, manual extras) to get data. Then tighten: move features behind Pro, test a hard paywall, shorten the trial. Keep the promise fixed. Grandfather existing users; Apple says not to remove features people already paid for (C§12).

### 7.6 Step 4: brainstorm delivery vehicles for every problem
- **Book:** List everything you could possibly do, including things you never would, and do it for each problem, because solutions to one spark ideas for others. Group by how many people one delivery serves. For the grocery problem: 1:1 shopping trips, group trips, recorded tours, a calculator, ready-made lists, pre-filled delivery carts. This is done once for a product that lasts years.
- **App:** 1:1 (founder DM, coach, AI tutor), small group (duel, partner, family league, cohort), 1:many (library, generated plans, leaderboards, widgets, pushes), and partner integrations as the "pre-filled cart" (deep links, calendar, Shortcuts, Health).

### 7.7 The delivery cube and the 10x / 1/10 test
- **Book:** Levers are personal attention, the effort asked of the customer, the live medium, the recorded format, and response speed and hours. Then ask what you'd do at 10x the price, and how you'd still get them results at 1/10.
- **App:** Tiers fall out of the cube. AI is the app shortcut: it feels 1:1 at close to 1:many cost, but check the inference cost of the 95th-percentile user. Real-time person-to-person services may bill outside IAP on iOS only; Google Play has no such exemption (C§11).

### 7.8 Solve every perceived problem; don't marry your method
- **Book:** The author lost sales by insisting clients cook at home, until he made a restaurant guide for an executive who ate out. Every obstacle became a template, so no single issue could block a sale.
- **App:** Treat each lost conversion or cancellation reason as a backlog item for a reusable mode, template or pack: a 2-minute quick mode, profiles, offline mode, widget-only reminders, cloud streak restore. Prioritise by frequency. A paywall line or FAQ entry that only reassures does not count as solving it.

### 7.9 Step 5a: trim on a cost/value grid
- **Book:** Cut high-cost/low-value items first, then low-cost/low-value. Keep low-cost/high-value and high-cost/high-value items. Judge value by the four drivers. Step an impossible idea back one notch at a time, or raise the price a lot.
- **App:** Cost = build hours + maintenance on two platforms x locales + per-user variable cost + store fee + review risk. Measure value with analytics. Keep high-cost/high-value items for the top tier.

### 7.10 Prefer one-to-many assets built once (why software is valuable)
- **Book:** A spreadsheet that took about 100 hours to build produced personalised meal plans in about 15 minutes each. Meal plans made in a week or two served thousands of gyms. Keep 1:1 only where it adds big value.
- **App:** Build generators and adaptive engines whose output feels bespoke, plus packs that each answer one objection. Prefer precomputed and cached content over generating it per request. Localisation multiplies content cost.

### 7.11 Step 5b: stack named, valued bundles
- **Book:** Each bundle has a solution line, an attractive name, a description, a stated value and the items it delivers. The weight-loss example has 7 bundles with a total stated value of $4,351, sold for $599 (about 7.3x). Values are anchored in money saved or time returned (200 hours a year, about 4 work-weeks). A review meeting is built in as the upsell moment.
- **App:**
  - Pro becomes 3-5 named systems, each solving a named problem, each with a defensible time- or money-saved figure.
  - Accountability becomes weekly reports and check-ins.
  - The upsell meeting becomes a day-14 or day-30 progress screen offering annual or lifetime.
- **Breaks:** Never put invented "worth $X" totals or fake regular prices on a store paywall (C§2, C§8). Keep them for internal reasoning and web pages, with a rationale.

### 7.12 The finished bundle: complete, unique, impossible to compare
- **Book:** It solves all perceived problems, feels one of a kind, and can't be compared with the business down the street.
- **App:** Sell the system, not a feature grid that invites checklist comparison. Price comparison never fully disappears in store search, so the name and method must do the work.

---

## F§8 Enhancing the offer: supply and demand (Ch. 11)

### 8.1 Context beats product (the gala)
- **Book:** A charity gala cut ticket supply while raising the price, auctioned one-of-a-kind items, and added bonuses when two bidders fought. Items that would struggle to fetch about $10k sold for about $100k, and about $5.4M was raised from 100 people.
- **App:** Run a second design pass on everything around the product: framing, launch sequence, promo calendar, capped premium layers, named bonuses, guarantee, name. It multiplies a good loop but can't rescue a weak one, because D1/D7 retention exposes it.

### 8.2 When demand rises, cut supply
- **App:** Apply this only to finite layers: human time, heavy AI use, community seats, live sessions, beta spots, cosmetic drops. When a finite tier fills, raise its price. After a demand spike, A/B test a higher price rather than running a sale.

### 8.3 Marketing moves the supply-demand curve (with a mass-market caveat)
- **Book:** More demand sells more units; restricted supply raises the price per unit. This assumes you aren't deliberately chasing mass penetration.
- **App:** Split your levers into demand dials (content, ASO, reels, referrals, naming, proof) and supply dials (caps, cohorts, tier gating, daily limits). The free tier is usually a reach game, so scarcity lives only on premium layers.

### 8.4 Desire dies when satisfied: ration on purpose
- **Book:** Citing Naval's idea that desire is a self-made pact to stay unhappy until you get the thing, the author concludes that we only want what we lack and that desire disappears once satisfied. So delay satisfaction and sell fewer units than you could.
- **App:** Rationing is native to apps: one puzzle a day, refilling lives, weekly drops, free AI message caps. Give the free tier slightly less than people want, and end sessions on an open loop.
- **Breaks:**
  - Heavy rationing on day 1 kills activation.
  - Rationing inside Pro brings refunds.
  - Keep it feeling like a fair rule, especially for children.

### 8.5 Whisper, tease, shout
- **Book:** Hint, then tease benefits, then announce the date about a week out, then open.
- **App:** Run the tease mostly outside the app: pre-order or pre-registration, an in-app event page, waitlist, TestFlight, reels, email. In the app, show at most a dismissible dated news card. Never show a dead feature tile; that is placeholder content under Apple 2.1, and hiding it from review breaks 2.3.1.

### 8.6 Pent-up demand compounds; selling the whole pyramid drains it
- **Book:** People who missed out want it more, especially once they see buyers win. Selling to everyone cheaply leaves nobody wanting.
- **App:** For lifetime deals, cohorts, coach seats and drops, run repeated sell-outs and make buyers' wins visible. Deep lifetime blowouts teach users to wait for deals.

### 8.7 Hormozi's law: delay the ask to enlarge the ask
- **Book:** A longer runway launches a bigger plane.
- **App:** It collides with the data: most trial starts happen on Day 0 (C§14). So keep the first ask early (an onboarding paywall with a trial) and delay the big asks (lifetime, top tier, upgrade to annual) until the user has invested.

### 8.8 The delicate dance: ravenous, not merely interested
- **App:** Calibrate the free tier with data. Track hunger signals (taps on locked features, paywall revisits, notify-me toggles). Starved users uninstall in seconds and leave 1-star reviews.

### 8.9 The five levers
- Scarcity cuts supply.
- Urgency lowers the threshold for acting.
- Bonuses raise demand and exclusivity.
- Guarantees reverse risk.
- Names re-stir demand and widen awareness.
- These are the fixed sub-steps of SKILL step 8.

### 8.10 Other persuasion forces belong to selling, not the offer
- **Book:** Commitment, status, peer pressure, celebrity and competition are part of selling, not the offer.
- **App:** Route them to growth and product design: streaks, leagues, share cards, creator endorsements. Be careful with young audiences and with partner or family visibility that one member could use to pressure another.

### 8.11 Implied demand and rarity x value
- **Book:** Authorities charge high fees because people assume their time is scarce. A buyer with a rare, consuming problem sees a supply of one solver. Example: a $50k day that produced $500k a month.
- **App:**
  - Show honest live demand signals: real counters, chart positions, Editors' Choice, rating counts, expert attachment.
  - A niche app that solves one acute, deadline-bound problem (exam or test prep) can charge 5-20x a general app.
  - Search keeps substitutes one tap away, so earn uniqueness through specificity.

### 8.12 Whoever needs the deal less holds the power
- **Book:** Turning down money signals confidence that can't be faked.
- **App:** Paywalls should read calm. No chains of escalating discount pop-ups. Count how many discounts a user sees before day 7. A/B test exit offers on LTV, not first conversion.

### 8.13 Free below the threshold, aligned stake above it
- **Book:** Teach everyone below a revenue level for free; take equity with the few above it.
- **App:** The free tier and free content serve the many. Premium and outcome-linked offers serve the few. Equity doesn't translate to consumer apps (F§16).

---

## F§9 Scarcity (Ch. 12)

| Book idea | App translation | Honesty test |
|---|---|---|
| Publicly stated fixed supply triggers loss aversion (the limited hoodie run) | "Founding lifetime: 500 total, 412 claimed" from a real tally | Is the cap enforced, never quietly reopened, and tied to a real lasting benefit? |
| Three types: limited slots, limited bonuses, never available again | Coach/cohort/beta seats; the first N annual buyers get a live session; seasonal badges and founder pricing | Retired items really leave, including from restore flows for non-owners |
| Limited drops: always sell out, about monthly, announce the sell-out | Monthly cosmetic, icon or challenge-pack drops sized to sell out; post "gone" in-app and on social | Selling cosmetics needs IAP; randomised drops need odds disclosure |
| Chanel ships 1-2 of each piece per store: every item is the last one | Rotating shop or weekly challenge-pack rotation | Items really rotate out |
| Total business cap plus waitlist, expanded 10-20% at a time, price raised each batch | Cap only the human or high-cost tier, enforced by a seat count (server, or a hand-switched Offering with no backend); hide the SKU when full | Stores can't cap subscriptions natively; the core subscription stays uncapped |
| Growth-rate cap (X new clients a week) | Weekly intake for human-reviewed plans or white-glove setup | Self-serve Pro has no weekly limit, so never fake one |
| Cohort cap (X per class) | "Bootcamp: 100 seats, starts the 1st" | Group sessions sold in-app use IAP (C§11) |
| Sell fewer seats than you could on high-ticket upsells | Live masterclass or tournament with seats below expected demand | Repeat and publicise the sell-out |
| Scarcity on free things (20 downloads a week plus a notify list) | Weekly batch of free Pro passes; "notify me" doubles as the push opt-in | Cap things with real cost; grant via offer codes or entitlements |
| Honest scarcity: publish real capacity ("81% full") | Live fill bars on capped layers; write down the capacity rule | Would you be comfortable if a user audited the counter? |
| Extreme scarcity: tiny, very expensive 1:1 access through a channel you don't hate | "Founder's line": 10-20 seats at about 10-30x annualised Pro | iOS only: real-time 1:1 calls can bill outside IAP; Google Play has no such exemption; in-app unlocks need IAP (C§11) |
| Once you leave, you can't come back | A grandfathered price that is lost if the user stays unsubscribed past Apple's 60-day resubscribe window; small tiers that don't re-offer seats | On iOS say "lost if you stay unsubscribed for more than 60 days", never "gone the moment you cancel" (C§4). Check Google's legacy-price-cohort behaviour before claiming anything on Android. Can't block re-subscribing to the core; decide this against your win-back policy |

The rule throughout: digital supply is infinite. Scarcity is honest only on human time, inference, seats, events, and runs or caps you genuinely enforce. If none exist, scarcity is "none" (C§8). No-backend implementations: F§17.4.

---

## F§10 Urgency (Ch. 13)

- **Scarcity vs urgency:** scarcity limits quantity; urgency limits time.
- **The book's four ethical forms:**
  1. Rolling cohorts
  2. Rolling seasonal urgency
  3. Pricing or bonus urgency
  4. Exploding opportunity

| Book idea | App translation | Compliance |
|---|---|---|
| Rolling cohorts: join now or wait for the next start; less frequent starts pull harder; start dates choreograph onboarding | Weekly league resets, monthly challenges, "you're in Monday's league", a scripted push/email sequence per cohort | Gate only the cohort layer, never the core app; a "someone dropped out" line only if literally true |
| Deadlines create the sales: 50-60% of a week-long launch lands in the last 4 hours (about the last 3% of the window); people who miss it were never buying | Final-24h banner and paywall timer, final-day email, last-4h push to opted-in users, local time zones; never extend | Promotional push needs opt-in (Apple 4.5.4); timers never reset; UK bans false "limited time" claims (C§8) |
| Missed the cohort: fast-track with a bonus, or frame the wait as an advantage | A catch-up placement test, or a "warm-up week" that sets the baseline before the start | Never make users wait for the core app; payment-plan flexibility mostly needs web |
| Rolling seasonal deadlines: the same offer in a new dated wrapper about monthly; local businesses should rotate wrappers often | A 12-month calendar (New Year reset, back to school, exam season, tax season, Black Friday) swapping Offerings, promotional text, in-app events, custom product pages | Reference prices must be genuine (EU Omnibus); in-app events need real content |
| Pricing/bonus urgency: the deal expires, not the service | Expiring bonuses (preferred) or a dated intro price; rotate about every 4 weeks | One intro offer per subscription group per user; offer types have eligibility rules (C§3) |
| Announce price rises to clear the pipeline | "Price rises Dec 1; lock in today's price while subscribed" plus grandfathering | Consent thresholds; the date must be real (C§4) |
| Exploding opportunity: real gains that decay with delay | Capture the user's own date (exam, interview, wedding, move, tax day, trip) and show sessions left before it | Only dates the user provided; never financial-gain urgency |

---

## F§11 Bonuses (Ch. 14)

### 11.1 Stack the offer
- **Book:** One offer is worth less than the same offer split into parts and stacked. The infomercial "but wait, there's more" works this way. Anchor the price to the core, then widen the value gap with each bonus. Anything you deliver but don't list is invisible.
- **App:** Name the core, then stack 3-5 named components on the paywall, with an expandable "everything in Pro" list. Every item must exist in the build (C§12). Use comparisons, not invented totals.

### 11.2 Add bonuses, never discount the core
- **Book:** Discounts teach people your prices are negotiable.
- **App:** On decline flows, test adding value before cutting price: a longer trial, a bonus month on annual, a bonus pack. Keep discounts for dated seasons and win-back. Judge on LTV and renewals.

### 11.3 Sequencing: ask, reveal after the yes, add one bonus per objection
- **Book:** One-on-one, reveal bonuses after the yes for a wow moment. After a no, add a bonus aimed at the stated obstacle and ask again, which works through reciprocity.
- **App:**
  - Post-purchase "you also unlocked" screen, which reduces remorse and refunds.
  - Decline screen keyed to the objection captured in onboarding.
  - Cap the later re-asks at value moments; nagging invites Apple 5.6 scrutiny and 1-star reviews.

### 11.4 Presentation rules (the book lists about 11)
1. Always offer bonuses.
2. Give each a name that carries a benefit.
3. Say how it relates to their problem.
4. Say what it is.
5. Say how it was made or found.
6. Say how it makes life faster or easier.
7. Give proof.
8. Paint the after-picture.
9. Attach a justified value.
10. Prefer tools and checklists to training.
11. Aim each one at an obstacle or the next problem.

Also: the bonuses' total should exceed the core, and scarcity or urgency can apply to the bonuses themselves.

**App bonus card:** benefit name, link to the problem, what it is, how it was made ("built from N answered problems", only if true), speed or effort claim, measured proof, after-picture, honest value reference (a real standalone IAP price or a comparison).

### 11.5 Tools beat training
- **App:** Interactive drills, generated plans, widgets, one-tap routines, templates and printable cheat sheets beat video courses. Watch per-use AI cost.

### 11.6 Each bonus kills an objection or solves the next problem
- **App:** Build an objection-to-bonus map. Two examples:
  - Skill or habit app: "I'll forget" > widget plus reminder; "I'm too slow" > placement test plus beginner track; "No time" > short mode plus streak freeze; "Will I improve?" > progress report; next problem > certificate, exam mode.
  - Couples or finance app: "My partner won't join" > free partner seat plus a 2-minute invite quiz; "I want some privacy" > private pots; "We'll just argue" > a neutral weekly summary; "Linking my bank feels risky" > manual mode first; next problem > a shared-goal planner.

### 11.7 Total bonus value should exceed the core
- **App:** Present the core as one strong thing and the extras as a stack that clearly outweighs it, but only with real standalone prices. Where bonuses have none (templates, reports), show objection coverage instead and report the dollar test as FAIL. Longer plans carry more bonuses. Don't pad the stack.

### 11.8 Scarce and urgent bonuses
- **Book:** Bonuses exclusive to this offer, a limited supply of a bonus, or a bonus that's lost if you don't buy today.
- **App:** Pro-only packs never sold separately; the first N annual buyers get live-event seats; a launch-week founder badge. Use purchase timestamps to deliver them.

### 11.9 Other people's products as bonuses
- **Book:** Non-competing partners give products or services for exposure to your buyers. In the pain-clinic example, partner perks alone outvalued the $400 offer and referral fees added about $350. Negotiate a group discount plus a commission (example: 30% off for customers, 40% commission to you).
- **App:** Non-competing app months via partner offer codes, workbook or tutoring discounts, indie cross-promos. Redeem by code with no user data shared. Linking out to external purchases is restricted outside the US (C§11).

### 11.10 The bonus vault
- **Book:** Build checklists, templates and scripts once; record every event; give a month of a higher service level as an upsell trial.
- **App:** Keep a vault of cheat sheets, compiled reels, recorded AMAs and challenge packs, delivered through remote config. Grant a top-tier month to annual buyers as a RevenueCat promotional entitlement on top of their paid Pro, so store billing is unchanged. Don't use a store offer on the higher-tier product: on iOS the upgrade is immediate and then auto-renews at the higher price.

### 11.11 Bonus or core? The wow factor
- **Book:** Pull out short, distinct, high-value items (checklists, infographics) as named bonuses rather than letting them get lost.
- **App:** Promote buried gems (a tips screen, a hidden chart) to named bonuses. Choose 3-5 and fold the rest into "everything in Pro".

### 11.12 Assembly
- **Book (end of Ch. 14):** Core plus scarcity plus urgency plus a bonus stack, then remove the remaining risk with a guarantee.
- **App:** Lead each screen with one urgency signal and one scarcity signal at most.

---

## F§12 Guarantees (Ch. 15)

### 12.1 Risk is the biggest objection
- **Book:** Reversing risk is the strongest single lever. Fladlien saw 2-4x conversion swings from the guarantee alone. Spend as long on the guarantee as on the deliverables.
- **App:** In apps the risks are:
  - a forgotten-trial charge
  - paying and not using the app
  - annual lock-in
  - difficulty
  - price rises
  - ads and privacy
  - poor AI output
  - a partner or family member who never joins (multi-user)

  The paywall's risk block is a core screen. Test its wording separately from price.

### 12.2 Refund maths
- **Book:** 100 sales at 5% refunds nets 95. 130 sales at 10% refunds nets 117, which is 1.23x.
- **App:**
  - Net multiplier = (paid_new x (1 - r_new)) / (paid_old x (1 - r_old)).
  - Break-even: (1 + lift)(1 - r_new) = (1 - r_old). Example: a 10% lift from a 2% base tolerates refunds up to about 10.9%.
  - Subtract the variable cost refunders consume.
  - Apple refunds reverse your proceeds, may arrive weeks later, and are noisy at indie volume.
  - Free-time guarantees cost forgone renewals, not refunds: see F§17.2.

### 12.3 Guarantee-only buyers make bad customers, so condition on success actions
- **App:** The conditions should be your activation metrics (sessions, streak, plan completion, reminders on, partner joined). Show progress toward qualifying. Apple may refund regardless of your conditions.

### 12.4 High delivery cost: use conditional or anti-guarantees
- **App:** AI inference, human coaches, paid APIs and licensed content are the exceptions to near-zero marginal cost. Cap usage during trials, or state that you add no refund of your own for generated output (store and legal refund rights still apply, C§5). Send consumption data on Apple refund requests (C§5).

### 12.5 Anatomy: "If you don't get X by Y, we will Z"
- **Book:** Without the "or what", it sounds weak.
- **App:** X is measured in-app, Y is realistic for an engaged user, and Z is payable on every platform and every plan shown.

### 12.6 The four families
Unconditional, conditional, anti-guarantee, implied/performance. Whatever you choose, state it boldly with a reason.

| Family | Book forms | App form | Platform notes |
|---|---|---|---|
| Unconditional | Full refund, half refund, refund plus costs, pay for a competitor, refund plus cash; "decide from the inside" framing | Free trial + a reminder before the first charge + easy cancel; on web or Play, a no-questions refund | At consumer prices the trial is the unconditional guarantee. State cancel-anytime and Apple's refund route as information, never as your named guarantee (C§8 legal-rights rule). Extra cash payouts need web rails |
| Conditional | Worth more than a refund, with success actions as conditions; ideally everyone qualifies and nobody claims | "Play 20 of 30 days; no improvement means 3 months of Pro free" | Pay out as free time that moves the store billing date. Apple renewal-date extension: immediate, up to 90 days, two per 365 days, only for active subscriptions with a paid period (not in a free trial or offer period, billing retry, or after expiry). Otherwise a free Apple offer code or promotional offer on the same product: it starts at the next renewal (months away on annual) and the user must redeem it; only one promotional offer can be active. Google `subscriptionsv2.defer`. A RevenueCat promotional entitlement does not pause store billing, so use it only for lapsed or web subscribers |
| Anti | All sales final, with a reason showing real exposure; also filters out uncommitted buyers | Consumables, generated output, one-shot packs: "we add no refund of our own, because each image costs real GPU" | Store and statutory refunds still apply: Apple decides iOS refunds, Google offers a 48-hour self-serve window, EU/UK withdrawal rights apply. Never write "non-refundable" or "all sales final" on a store surface. The reason must be true |
| Implied/performance | Per result, revenue share, profit share, ratchets, hybrid minimums | Creator platforms, savings fintech, B2B AI priced per resolution | Only if the app moves or earns money for the user; IAP can't bill variable amounts afterwards, so this needs web or your own payment flow |

### 12.7 Every type in the book, translated
- **Service** (the author's favourite): keep delivering free until the result arrives. **App:** "Pro free until you hit X". It is close to free for non-AI apps. For an active auto-renewer, grant the time through a rail that moves store billing (F§12.6 Conditional row). Don't use a RevenueCat promotional entitlement for them, because it leaves store billing running. Entitlement grants are fine for lapsed and web subscribers.
- **Modified service:** another fixed period, at least 2x the original. **App:** "Meet the conditions with no gain: 2x your period free". Extensions cap each grant at 90 days, so pay longer periods with a free offer code or promotional offer on the same product, and tell the user the free period starts at their next renewal.
- **Credit:** the money becomes credit toward something else you sell; best for upsells. **App:** an unhappy add-on buyer gets Pro time (via extension, a free offer code or promotional offer, or defer if they are auto-renewing) or credits instead.
- **Personal 1:1:** you work with them until they succeed, with strict contingencies. **App:** for top-tier or lifetime buyers, a founder review of their stats if they're still stuck after the conditions. Cap the number of claims.
- **Refund plus outside costs / hotel and airfare / wage** (income / 1,960 hours): covers costs around the purchase. **App:** only for apps tied to outside costs (exam retake fees, setup calls). Needs cash rails outside the store.
- **Outsized refund (2-3x or a big payout):** Fladlien's $25k store buyback on a $2,997 course, about $2.75M net gain after 10 payouts. **App:** usually translate it into access ("3x your time back"). Cash versions only for web-sold, high-commitment products.
- **Release from contract:** **App:** stores already let users stop auto-renew. Say "cancel anytime in Settings" as plain information, never as your named guarantee, because presenting legal or store-default rights as a distinctive feature is banned in the EU and UK (C§8). State a tap count only after counting it on a device.
- **Delayed second payment until the first outcome:** **App:** store trials are fixed lengths, so approximate it with a trial longer than the median time to the aha moment, or a promotional entitlement until activation for a user who has not yet subscribed. Its main value is forcing you to define and instrument activation.
- **First-outcome:** cover their running costs until the first win. **App:** "Credits are on us until your first result you're happy with", with a cap.
- **Satisfaction on what you control, plus a best/worst-case close:** the author guaranteed a stated dollar value of service, not the weight lost; 2 claims in about 4,000 sales. **App:** guarantee what the app controls (fresh adaptive sets daily, no ads). Close with "best case you get the result; worst case you cancel and keep what you learned".
- **Breadth:** broad guarantees for cheap consumer offers, specific ones for expensive B2B. Consumer apps should be broad and loud.
- **Stacking and future pacing:** unconditional + conditional, or sequential milestones. **App:** trial + reminder, plus a results promise, plus a price lock, alongside a dated, personalised milestone chart in onboarding. The projections must be honest.
- **Design your own:** list fears (from reviews, cancellation reasons, support), reverse each one, and start with service-style guarantees, which remove the fear of refunds and keep you committed to results. Then either keep them and scale, or loosen toward broader guarantees as proof builds, to grow volume. Guarantees amplify a good product and backfire on a bad one.

### 12.8 Name the guarantee
- **Book:** Not "satisfaction guaranteed". Use vivid, odd imagery people retell.
- **App:** Write it in the brand or mascot voice (in the in-app register if the brand has several) and match the age rating. The badge can appear on the paywall, onboarding, ads, promotional text and the website. It can't appear in the store name, subtitle, screenshots or previews (Apple 2.3.7). Badge text must match the per-plan payout table.

---

## F§13 Naming (Ch. 16)

### 13.1 Names drive response
- **Book:** The same offer can draw 2-10x the response with a better name. People favour what resembles themselves (implicit egotism): a "six-week stress-release challenge" beats a "float-tank session".
- **App:** Names appear in many places:
  - app name and subtitle
  - screenshot captions
  - ad hooks
  - paywall headline
  - plan and tier names
  - programs, challenges and in-app events
  - features and pushes

  Echo the identity the user gave in onboarding back in their plan name.

### 13.2 Offer fatigue: change the wrapper, never the offer
- **Book:** Small markets saturate quickly. The book says about $20 reaches 1,000 people and that 200k people cost about $10k to reach once. At its own $20 per 1,000 rate that is about $4k, so use the method (audience size x CPM), not the figure. Offers last years; when one tires, rename it.
- **App:** Ad creative tires within weeks and niche audiences saturate. Rotate campaign wrappers (seasonal challenges, in-app events, custom product pages, paywall headline, program name) over the same Pro. Don't keep renaming the app itself. Promotional text changes without review.

### 13.3 MAGIC
Use 3-5 of the 5 components; shorter is punchier, and the order is flexible.
- **M = attention**
- **A = discrimination** (who it's for)
- **G = purpose**
- **I = timeline**
- **C = method**

| Part | Book | App | Watch out |
|---|---|---|---|
| Magnetic reason why | Why this offer now: free, % off, season, opening, anniversary, holiday; any reason you believe | Launch, major update, app birthday, New Year, back to school, exam or tax season, a real usage milestone | The reason must be true; "free" and "% off" never go in store titles, screenshots or previews |
| Announce avatar | As specific as possible, but no more; hyperlocal converts better locally | Profession, exam, life stage (new couple, new parent), language and locale | Avatars go in campaigns and custom product pages, not the app title; naming children triggers kids rules |
| Give a goal | The dream outcome in a word or phrase, tangible | The outcome in users' own words | Grades, IQ, health or income claims draw scrutiny |
| Indicate an interval | Duration; use it wherever compliance allows, but don't pair a quantified result with a deadline where platforms forbid it (the book contrasts a money figure in N days with a first sale in N days) | Process durations ("7 minutes a day", "21-day sprint") or unquantified milestones ("your first 7-day streak") | Never a quantified result (money, weight, score gain, IQ) with a deadline |
| Complete with a container | Challenge, bootcamp, blueprint, sprint, accelerator, system, reset, and so on | Challenge, Sprint, Bootcamp, Path, Season, League, Ladder, Plan, Quest | The container must exist as real structure (start, end, progress, finale) |

### 13.4 Rhyme and alliteration
- **Book:** Nice to have, never forced.
- **App:** Say names out loud for reels. Rhymes rarely survive translation, so mark each name as surviving or not and give a per-locale rule (native descriptive name) where it doesn't. Keep edgy names to the out-loud register (ads, social) if the brand separates registers.

### 13.5 Test names
- **Book:** Run 2-3 names, crown the winner as the control, keep challenging it. Nobody can predict winners.
- **App:** Test via Apple product page optimisation, custom product pages, Google store listing experiments, ad sets and paywall experiments. Use ad CTR as a cheap first filter (also pre-build, SKILL step 10). At indie traffic, test big differences only.

### 13.6 Name the sub-items too
- **App:** Branded, benefit-led names for every paywall bullet, each with a plain descriptor, because Apple requires subscriptions to describe clearly what is included.

### 13.7 Fatigue rotation order (light to heavy)
1. Creative
2. Body copy
3. Headline / offer wrapper
4. Goal or theme within the name
5. Seasonal reason
6. Duration
7. Enhancer (free or discount element)
8. Monetisation structure

- **Book:** Usually only the first few need changing. Once an offer makes money, change it rarely.
- **App:** Steps 1-2 cover ads, store creative, screenshots, promotional text and subtitle. Steps 3-7 can change remotely through RevenueCat Offerings. Step 8 means new products, review and existing-subscriber price cohorts.

### 13.8 First traction and "multiple aces"
- **Book:** Launch the structure you believe in most and stick with it while your skill grows. Keep several proven offers you can rotate.
- **App:** Start with one paywall and one primary wrapper. Build a library of proven seasonal and avatar wrappers as Offerings. Too many simultaneous variants splinter low traffic.

### 13.9 Local vs national
- **Book:** Local offers are easier to get working but fatigue fast; never change the stack, only how it looks.
- **App:** A hyper-niche app (one exam, city, profession or language) behaves like a local business: it converts well and saturates fast. Each locale has its own fatigue clock. Replace face-to-face trust with the founder's face, native-language localisation, local proof and regional prices.

---

## F§14 Execution (Ch. 17 and closing)

### 14.1 The first $100k
- **Book:** The first $100k is the hardest. When he had it as personal cash (about 3 years of runway at his costs), it felt like relief, not joy. A first grand slam offer should be enough to get there. Persist.
- **App:** Counting $100k of **fee-net revenue at shelf price** (after the store fee, before VAT removal and income tax; App Store Connect proceeds will be lower in VAT storefronts), divide the target by (1 - fee) to get gross customer spend. One example at a 15% fee ($100k fee-net needs about $117.6k of customer spend):
  - about 1,307 lifetime sales at $89.99 ($76.49 net each)
  - or about 3,923 quarterly payments at $29.99 ($25.49 net)
  - or about 39,370 weekly payments at $2.99 ($2.54 net)

  For **take-home cash**, also divide the target by (1 - VAT share of the price) in storefronts where the price includes VAT, and by (1 - your income-tax rate). Revenue in RevenueCat isn't cash in your account: payouts lag and refunds claw back.

### 14.2 The book's 11-point recap = the skill order
1. Don't be a commodity.
2. Pick a growing market and niche down.
3. Charge a lot.
4. Use the four value drivers to justify it.
5. Build the offer in five steps.
6. Stack it, deliver it and keep it profitable.
7. Scarcity.
8. Urgency.
9. Bonuses.
10. A creative guarantee.
11. A resonant name.

The enhancement recap adds that the guarantee also drives usage, which in apps means retention.

### 14.3 The closing test
- **Book:** Great marketing can't rescue a weak offer. Compete on value, not price.
- **App:** The final gate: would the avatar feel foolish dismissing this paywall? Acquisition (ASO, paid, social) and the full money model (upsells, downsells, free-tier monetisation) are out of scope here; note them for later work. Check whether first-week revenue per payer covers CPI.

### 14.4 Multi-modal learning tip (Ch. 2 aside)
- **Book:** Read and listen at the same time for better retention.
- **App:** At most a bonus idea (an audio or listen mode). The evidence is mixed, so make no claims.

---

## F§15 App levers the book doesn't cover (use in steps 7-10)

| Lever | Why it matters | Where |
|---|---|---|
| Paywall placement and model (hard / freemium / reverse trial) | Placement does the timing a salesperson would; hard vs freemium D35 conversion differs about 5x | Step 9, C§14 |
| Onboarding as the sales call | Day-0 dominates trial starts | Step 9 |
| Personalisation quiz | Raises likelihood; answers must change something | Step 9 |
| Trial design | Built-in risk reversal and urgency; length changes conversion and renewal | Steps 7, 8d |
| Store page as the ad | Custom product pages, product page optimisation, in-app events deliver market, name and urgency to cold traffic | Steps 1, 8, 10 |
| Ratings prompts | The app's social proof; strict rules | Step 9 |
| Cancellation retention messaging and win-back offers | A last offer at the moment of churn; month 1 holds the biggest share of annual cancellations | Step 10 |
| Involuntary churn recovery | Grace periods and account hold; Google loses more to billing failures | Step 7 |
| Price-change mechanics and grandfathering | Decide whether "raise prices and tell the pipeline" works without silent expiries | Step 7 |
| Regional pricing | User-geography LTV differs | Step 7 |
| Commitment and instalment billing | Lower visible monthly price, annual economics | Step 7 |
| US web checkout | Lower fees, real money-back; merchant-of-record duties | Steps 7, 8d |
| Kids and teens | Changes the paywall, analytics and data design | Steps 0, 9 |
| Multi-user and household pricing | Value exists only once the second person joins; cross-platform access needs your own entitlement | Steps 0, 4, 7, 9, 10; F§17.5 |
| Sensitive data and regulated categories | Declarations, privacy labels, organisation accounts, credentialed advice | Steps 0, 6, 11; C§16 |
| Experimentation velocity | Remote paywalls and onboarding replace sales-call iteration | Step 10 |

---

## F§16 Judged not applicable or heavily modified (with reasons)

| Book idea | Status | Reason |
|---|---|---|
| "Pay as you earn" or pay-after-results terms (the dad conversation, agency show-up pricing) | Not applicable in IAP | Store billing can't charge based on later outcomes. Only for money-touching apps billing on the web or in their own payment flow (F§12.6) |
| 100x niche price multipliers | Modified to 2-5x | Store prices are public and anchored low; consumer elasticity |
| Be the most expensive in the market (Kennedy; Gym Launch at 3x the top rival) | Modified to top quartile or highest, unless a reason is written down | Store search shows prices side by side and ranking rewards installs |
| Selling fewer units of the core to raise price | Not applicable to the core subscription | Infinite supply and download-driven ranking; applied only to finite layers |
| Refund plus extra cash, refund plus ad spend, hotel and airfare, wage guarantees | Mostly not applicable | Store refunds only ever return the price paid; extra payouts need web rails, verification and tax handling |
| Outsized 2-3x cash refunds | Modified to access multiples | Same reason; cash versions only for web-sold, high-commitment products |
| "All sales final" anti-guarantee | Modified | Store-billed sales can't be made final: Apple decides iOS refunds, Google has a 48-hour self-serve window, EU/UK withdrawal rights apply. Becomes "we add no refund of our own", with a true reason |
| Free-time payouts as a RevenueCat promotional entitlement for active store subscribers | Modified | An entitlement doesn't pause store billing, so active auto-renewers get free time via an eligible Apple renewal-date extension, a free Apple offer code or promotional offer on the same product (starts at the next renewal, user redeems), or Google defer; entitlements only for lapsed or web users |
| Inventing a reason for an anti-guarantee or a promo | Rejected | App Review honesty rules and consumer law; real reasons only |
| Printed "total value $X" stacks and strike-through regular prices on store paywalls | Rejected on store surfaces | Misleading-pricing risk (Apple 2.3, 3.1.2; EU Omnibus); kept for internal reasoning and web with a rationale |
| Bonus total must exceed the core | Modified | Only where bonuses have real standalone prices; otherwise objection coverage, and the dollar test is reported as FAIL rather than padded |
| Live re-ask loop and bonuses revealed after a verbal yes | Modified | No salesperson; becomes a post-purchase reveal plus one decline screen with capped re-asks |
| Once out, never back, for the core subscription | Not applicable | Users can always re-subscribe through the store. Only price locks (honest iOS wording: lost if unsubscribed for more than 60 days, since Apple preserves the price for a resubscribe within 60 days of expiry) and small capped tiers |
| Equity or revenue share instead of fees | Not applicable to consumer apps | No business outcome to share; only the alignment principle carries over |
| Release-from-contract guarantee as a differentiator | Already the default; information only | Stores let anyone cancel auto-renew; state it plainly, never as a named guarantee (EU/UK ban on selling legal rights as a feature) |
| Hyperlocal neighbourhood naming | Modified | Becomes locale and language localisation plus niche custom product pages |
| Ticket and in-person social forces at the gala (status, peer pressure, celebrity) | Out of offer scope | The book also routes them to selling; here they go to growth and product design |
| The author's benchmarks (36:1 ROAS, $1.5M/month run rates, 35% upsell, 158-gym survey) | Not targets | Service-business track record; use your own cohort data |
| The book's reach-cost figure ($10k for 200k people at $20 per 1,000) | Corrected | Its own rate gives about $4k (F§13.2); use audience x CPM |
| The 22.4x agency multiple | Kept, with a note | It checks out as $112k vs $5k upfront; only the rounded factors (2.5 x 2.5 x 4 = 25) don't match (F§1.13) |
| Moving in with the client as the ultimate overdelivery | Modified | Kept only as the step-back ladder starting point |
| Multi-modal reading tip | Not offer design | At most a bonus idea, with no claims |
| Delayed second payment tied exactly to activation | Approximated | Store trials have fixed lengths |

---

## F§17 Runner formulas and playbooks (not from the book)

### 17.1 Estimating average paid periods
- Paid periods ≈ 1 + r1 / (1 - r), where r1 = first-renewal rate and r = the later per-period renewal rate. Survivors churn less, so r ≥ r1.
- Calibrate r so that r1 x r^(n - 1) ≈ the C§14 day-380 retention row for the nearest plan type, with n = billing periods in about 380 days. Tag the result [B].
- Monthly with trial, example: r1 = 62.8% (5-9 day trial), day-380 = 14.2%, n ≈ 12, so r ≈ 0.87 and paid periods ≈ 1 + 0.628 / 0.13 ≈ 5.8 [B].
- Annual: r1 ≈ 27-28% (C§14 one-year retention of yearly subscribers); with no later-year data assume r ≈ 0.5 [A], giving about 1.5 periods. Use 1.3 as the conservative provisional figure in SKILL step 1.
- Weekly: C§14 has no first-renewal row. Use your own data, else 10 paid weeks [A], and sanity-check against the weekly day-380 row (5.5%).
- Lifetime: 1 period.
- Variable cost per payer includes revenue-share tools (RevenueCat, C§1) and third-party API fees for the 95th-percentile user.

### 17.2 Guarantee cost and the claim runbook
- **Free-time guarantee cost** per payer = claim rate x periods given free x net price per period. Break-even lift = cost / (LTGP - cost). Size Z per plan so cost stays below about 10% of that plan's LTGP.
- Example: a 90-day payout on a weekly plan is about 13 x $2.54 ≈ $33 per claimant, more than a 10-week weekly LTGP of about $25, so give weekly a shorter payout (e.g. 28 days).
- **Refund-based guarantee:** (1 + lift)(1 - r_new) = (1 - r_old); with no history take r_old from the C§14 category or paywall-type refund row [B].
- **Claim runbook fields:**
  1. Eligibility: where it is computed (on device, in analytics, on a server) and which events prove the conditions.
  2. Claim path: an in-app button that opens a prefilled email or form carrying the app user ID and the evidence.
  3. Verification source: analytics events or RevenueCat customer history.
  4. Payout: Apple App Store Server API "extend renewal date" (in-app purchase API key, reason code for customer satisfaction), or an Apple offer code sent to the user; Google `subscriptionsv2.defer` with a service account; RevenueCat promotional entitlement for lapsed or web users only.
  5. Turnaround target, expected claims a month, and minutes per claim.
  6. User messaging: when the free time starts (immediately for extension or defer; next renewal for offer codes and promotional offers), and a reminder if they must redeem.

### 17.3 Sample size for paywall tests
- n per arm ≈ 16 x p(1 - p) / Δ² (80% power, 5% two-sided). Equivalently, the minimum detectable effect ≈ 2.8 x sqrt(2p(1 - p) / n).
- p = 3%, Δ = 3 points: about 520 per arm. p = 8%, Δ = 4 points: about 740 per arm.
- If the detectable lift at your weekly traffic exceeds about 50% relative, run only big swings, or a dated before/after with a holdout.

### 17.4 No-backend implementations
- **End dates:** RevenueCat Offering metadata or remote config, read by the app; timers count down to that fixed date and never reset.
- **Caps and counts:** either switch the Offering by hand when the cap fills and show the cap without a live count, or point a RevenueCat webhook at a serverless function that tallies purchases and serves static JSON.
- **Guarantee eligibility:** compute on device, include the evidence in the claim email, and pay out by hand through App Store Connect, Play Console or a small script.

### 17.5 Multi-user offers
- Name who must join for the value to exist and who pays. Track the second user's join as the north-star metric.
- Pricing: per user or per household. Family Sharing works only for iOS users in the same family and can't be turned off once enabled; across platforms, grant the second member access through your own account system (C§12).
- Onboarding: deliver a first win solo, then the account step and the invite; test whether the invite goes before or after the paywall.
- Safety: private-by-default spaces, no covert visibility, a clean exit (leave the shared account, split or delete data), and opt-in for any partner nudges or monitoring.
