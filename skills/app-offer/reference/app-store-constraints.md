# App store constraints and benchmarks

**As of: 2026-10-28.** Store rules, court rulings, state laws and benchmark reports change often. **Re-verify every rule and number you rely on before anything ships: prices, trial terms, claims, guarantees, link-outs, minors, sensitive data.** Items marked UNVERIFIED could not be confirmed from a primary source.

Key sources:
- Apple App Review Guidelines: https://developer.apple.com/app-store/review/guidelines/
- Apple subscriptions: https://developer.apple.com/app-store/subscriptions/
- Google Play Subscriptions policy: https://support.google.com/googleplay/android-developer/answer/9900533
- Google Play Metadata policy: https://support.google.com/googleplay/android-developer/answer/9898842
- RevenueCat State of Subscription Apps 2026: https://www.revenuecat.com/state-of-subscription-apps
- Adapty State of In-App Subscriptions: https://adapty.io/state-of-in-app-subscriptions/

---

## C§1 Fees and proceeds

| Item | Rule | Source |
|---|---|---|
| Apple standard | 30%; falls to 15% once a subscriber has a year of paid service (extension days don't count toward the year) | https://developer.apple.com/app-store/subscriptions/ |
| Apple Small Business Program | 15% from the start for developers under $1M in proceeds | https://developer.apple.com/app-store/subscriptions/ |
| Google Play subscriptions | New fee tiers announced 2026-03-04, rolling out in the US, UK and EEA from 2026-06-30. Auto-renewing subscriptions pay a 10% service fee at every revenue level, plus a 5% billing fee when using Play Billing | https://support.google.com/googleplay/android-developer/answer/112622 |
| Google Play one-time purchases (lifetime) | Reported as 10% on the first $1M of annual earnings, then 20% (new installs) or 25% (existing installs), plus 5% billing. Google's Help Center table is ambiguous on the under-$1M rate, so confirm in Play Console before modelling lifetime LTGP | https://support.google.com/googleplay/android-developer/answer/16954621 |
| Proceeds vs shelf price | App Store Connect and Play report proceeds net of VAT in storefronts whose prices include VAT, so shelf price x (1 - fee) overstates dashboard proceeds there | Apple/Google developer docs |
| RevenueCat | Free up to $2.5k monthly tracked revenue, then about 1% of tracked revenue. Include it in variable cost. Re-verify on the pricing page | https://www.revenuecat.com/pricing |
| Payouts | Apple pays about 45 days after the fiscal month; Google pays monthly. Refunds claw back proceeds | Apple/Google developer docs |

LTGP math: use net proceeds (price x (1 - fee)), minus VAT where the storefront price includes it, minus variable cost.

## C§2 Paywall disclosure and subscription rules

| Rule | Consequence | Source |
|---|---|---|
| Apple 3.1.2(a): auto-renewables must deliver ongoing value, run at least 7 days and work across the user's devices. When moving a paid app to subscriptions, you can't remove features buyers already paid for | Rejection | https://developer.apple.com/app-store/review/guidelines/ |
| Apple sign-up screen must show: subscription name, duration, what's included, full localised renewal price, restore/sign-in, Terms and Privacy links, and for trials the trial length and what is charged after. **The billed amount is the most prominent price**; per-month equivalents and savings are smaller | Rejection (3.1.2(c), Schedule 2) | https://developer.apple.com/app-store/subscriptions/ |
| Apple 3.1.2(b): users must not be able to accidentally subscribe to several variants of the same thing; upgrades and downgrades must be seamless | Rejection | Guidelines |
| Google: a visible dismiss or "no thanks" when the app is usable without subscribing; say whether a subscription is required; no flows that cause accidental subscriptions; trial charge text must be legible and fully localised | Policy violation, removal | https://support.google.com/googleplay/android-developer/answer/9900533 |
| Google: an annual plan that prominently shows a monthly price is a listed violation | Strike, removal | Same |
| Google: benefits must be truthful; promotions must show when content is available without a subscription; benefits that drop sharply after the first period are a violation | Violation | Same |
| Apple 3.1.2(c): clearly describe what the user gets before asking them to subscribe. Apple 2.3.2: metadata must say whether featured items cost extra. Apple 5.6: don't charge for features that aren't delivered | Rejection / removal | Guidelines |
| Apple 5.6 Code of Conduct: no tricky price increases and no tricking users into purchases | Removal, termination | Guidelines |

## C§3 Trials, intro offers, promotional offers, offer codes, win-back

| Item | Rule | Source |
|---|---|---|
| Apple introductory offers | One per person per subscription group. One current and one future offer per storefront. New overlapping offers overwrite existing ones, and offers can't be edited once created. Free-trial lengths: 3 days, 1 or 2 weeks, 1, 2, 3 or 6 months, or 1 year | https://developer.apple.com/help/app-store-connect/manage-subscriptions/set-up-introductory-offers-for-auto-renewable-subscriptions |
| Apple promotional offers | Up to 10 per subscription, only for current or previous subscribers. Apply to all storefronts. Only the price can be edited after creation. Accepted in your app UI with a server-generated signature. Only one promotional offer can be active at a time; accepting another replaces the current one at the next billing event. A promotional offer on the subscription the user already has starts at the next billing event (C§5) | https://developer.apple.com/documentation/storekit/implementing-promotional-offers-in-your-app |
| Apple offer codes | Eligibility: new, existing (currently subscribed, auto-renew on) or lapsed subscribers. One-time-use codes come in batches of 500-25,000 and expire within 6 months. Custom codes allow up to 25,000 redemptions at a time with an optional expiry (at most 6 months if set). Expiry dates can't be edited. 1M redemptions per app per quarter; up to 10 active offers per subscription; one code per customer per offer. Existing subscribers can only redeem codes at the same service level or an upgrade; for an already-subscribed customer the code may apply to the next renewal period. This gives you an auditable real cap for honest scarcity, and a guarantee payout rail (C§5) | https://developer.apple.com/help/app-store-connect/manage-subscriptions/set-up-subscription-offer-codes/ ; https://developer.apple.com/documentation/storekit/supporting-subscription-offer-codes-in-your-app |
| Apple win-back offers | Configured per product. Eligibility is set by paid duration (1-24 months or 3/4/5 years), a lapse window (1-24 months) and an optional 2-24 month wait between redemptions. Shown in an in-app sheet on iOS 18+ and on App Store surfaces | https://developer.apple.com/help/app-store-connect/manage-subscriptions/set-up-win-back-offers/ |
| Google | Offers can be scheduled per base plan. Trial lengths run from 3 days to 3 years. Intro pricing must not hide the post-intro charge: before enrolment, state the trial length, the price, when it converts, and how to cancel | https://support.google.com/googleplay/android-developer/answer/9900533 |
| Apple 3.1.1 (non-subscription apps) | A trial must be a free non-consumable named "XX-day Trial" | Guidelines |

## C§4 Price changes

| Store | Rule | Source |
|---|---|---|
| Apple | Subscribers must consent to an increase if any of these apply: the region requires it; the increase is more than 50% AND more than about US$5 per period (non-annual) or about US$50 per year (annual); or there was another increase in the past 12 months. Otherwise they only get notice. Subscribers who don't consent expire. You can preserve existing subscribers' current price (grandfather them). **A preserved price survives if a lapsed subscriber resubscribes within 60 days of expiry**, so a price lock is honestly "lost if you stay unsubscribed for more than 60 days", not "lost the moment you cancel" | https://developer.apple.com/help/app-store-connect/manage-subscriptions/manage-pricing-for-auto-renewable-subscriptions |
| Google | Increases are opt-in by default, with 37 days' lead time; users who don't accept are cancelled. Opt-out increases are allowed only in some countries: once per base plan per region per 365 days, capped at the greater of 50% or US$0.17/day, with 30 or 60 days' notice, an in-app notice at least 30 days ahead, and ToS that reserve the right. Existing subscribers stay in a legacy price cohort by default. Check what happens to the legacy price when a subscriber cancels and resubscribes before making any "lost on cancel" claim for Android | https://support.google.com/googleplay/android-developer/answer/12154973 |

Protocol: raise prices for new subscribers first, grandfather existing subscribers, announce a real date, and make at most one increase per 12 months.

## C§5 Refunds and the payout rails a guarantee can use

| Platform | What the developer can do | Source |
|---|---|---|
| Apple | **Apple decides refunds; the developer cannot issue them.** You can open the refund-request sheet (`beginRefundRequest`) and send consumption data within 12 hours of a CONSUMPTION_REQUEST (with user consent for personal data). Promising money back on iOS that you can't deliver is a misleading-claim risk (2.3.1, 5.6). A specific rejection precedent is UNVERIFIED | https://developer.apple.com/videos/play/wwdc2021/10175/ |
| Apple 5.6.4 | Excessive complaints, negative reviews and refund requests count against Code of Conduct compliance | Guidelines |
| Apple renewal-date extension | 1-90 days per request, at most two per customer within any 365 days. Only for active subscriptions with at least one paid period; NOT available during a free trial or free offer period, in billing retry, in a grace period with a past expiry date, or after expiry. It moves the billing date immediately, can't be reversed, and also extends Family Sharing members. Apple documents it mainly as compensation for outages; send the customer-satisfaction reason code for a guarantee payout | https://developer.apple.com/documentation/appstoreserverapi/extending-the-renewal-date-for-auto-renewable-subscriptions ; https://developer.apple.com/documentation/appstoreserverapi/extendreasoncode |
| Apple offer codes / promotional offers as payouts | When an active subscriber redeems a free promotional offer or offer code for the product they already have, the free period starts at their next billing event, replacing paid renewals with no double charge. On an annual plan that can be months away, so guarantee terms must say "your free months start at your next renewal date". The user must redeem it (a signed promotional offer in your app, or a code via the redemption sheet), so track redemption and remind them. Use it for payouts over 90 days, for users not eligible for an extension, or once the year's two extensions are used | https://developer.apple.com/documentation/storekit/implementing-promotional-offers-in-your-app ; https://developer.apple.com/documentation/storekit/supporting-subscription-offer-codes-in-your-app |
| Google | The developer can issue full or partial refunds and revoke access through Play Console or the API (`subscriptionsv2.revoke` with prorated refund). Users can request a refund themselves through Google Play within 48 hours of purchase; after that, refunds are up to the developer's policy and the law. `subscriptionsv2.defer` delays billing by 1 day to 1 year per call. Cancelling doesn't refund the current period by default, though some countries require prorated refunds. You must provide an in-app way to manage or cancel | https://support.google.com/googleplay/android-developer/answer/9900533 ; https://support.google.com/googleplay/answer/15574908 |
| Statutory rights (EU/UK) | Customers have a 14-day cancellation right for digital content unless they expressly waived it on immediate supply. The UK subscription regime (from 2027-01-01) adds a cooling-off period after a trial or renewal. So never write "non-refundable" or "all sales final" on a store surface; an anti-guarantee can only say you add no refund of your own on top of the store's process and the law | https://www.apple.com/uk/legal/internet-services/itunes/ ; https://cms.law/en/gbr/legal-updates/uk-subscription-contracts-the-government-publishes-the-missing-detail |
| RevenueCat promotional entitlements as payouts | Grants access without touching store billing, so an active auto-renewer is still charged. Use it as a free-time payout only for lapsed users or web (non-store) subscribers, or as an add-on grant on top of a paid plan (e.g. a top-tier month) | RevenueCat docs |
| Web checkout (US) | You control refunds fully and become merchant of record (refunds, tax, ROSCA and state auto-renewal laws including California's, disputes) | C§8, C§11 |
| Cancel links | Apple `showManageSubscriptions`; Google Play subscription center link | Apple/Google docs |

## C§6 Metadata and naming

| Rule | Source |
|---|---|
| Apple 2.3.7: the name must be unique, keywords accurate, and there must be no trademarks, pricing or irrelevant phrases. App name is 30 characters or fewer. **Names, subtitles, screenshots and previews may not include prices or terms**, so guarantee terms, payouts and "free"/"% off" stay out of them | https://developer.apple.com/app-store/review/guidelines/ |
| Apple 2.3.8: "For Kids" and "For Children" are reserved for the Kids Category; outside it, metadata may not imply children are the main audience | Same |
| Google Metadata: title of 30 characters or fewer; no emojis or repeated special characters; no rank claims ("#1", "Popular"); no price or promotion text ("10% off", "free for limited time") or Play program references in the title, icon or developer name; no unattributed testimonials in the description | https://support.google.com/googleplay/android-developer/answer/9898842 |
| Google Subscriptions: SKU names must describe the product accurately; naming an auto-renewing product "Free Trial" is a listed violation | https://support.google.com/googleplay/android-developer/answer/9900533 |
| Apple 4.3 (spam): near-duplicate niche apps get rejected, so use one app with tracks and custom product pages | Guidelines |
| Store testing surfaces: Apple product page optimization (up to 3 treatments, 90 days); custom product pages (up to 70, each can carry its own keywords); in-app events (up to 5 featured, reviewed, must be a genuine happening). Google custom store listings and store listing experiments; Promotional Content | https://developer.apple.com/app-store/product-page-optimization/ |

## C§7 Claims, proof and reviews

| Rule | Source |
|---|---|
| Apple 2.3.1: marketing content or services the app doesn't offer, or a false price, can lead to removal and account termination | Guidelines |
| Google Deceptive Behavior: no misleading claims in the title, icon, description or screenshots; a "for entertainment" label does not exempt a claim | https://support.google.com/googleplay/android-developer/answer/17006354 |
| Apple: reviews may appear in marketing only with the reviewer's permission, and ratings only if they accurately reflect the current rating | https://developer.apple.com/app-store/ratings-and-reviews/ |
| Apple 5.6.1: request ratings only through the provided API, at most 3 times in 365 days; no custom review prompts | https://developer.apple.com/app-store/ratings-and-reviews/ |
| Google In-App Review: don't trigger it from a button, don't ask questions before it, show the card unmodified; a quota applies | https://developer.android.com/guide/playcore/in-app-review |
| Apple 3.2.2(x): you can't force rating, reviewing or downloading other apps to unlock content; incentivised reviews can lead to expulsion | Guidelines |
| FTC Consumer Reviews and Testimonials Rule (16 CFR Part 465, effective 2024-10-21): no fake or AI-written reviews or testimonials, no incentives conditioned on positive sentiment, insiders must disclose their connection, no review suppression; civil penalties per violation. Disclose any incentive behind a testimonial | https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials |
| Cognitive and brain-training claims: in January 2016 the FTC settled with Lumos Labs (Lumosity) for $2M (a $50M judgment suspended) over claims of better performance at school, work and everyday tasks, slower age-related decline and protection against dementia, plus testimonials solicited through contests without disclosure. Claims beyond the trained skill need competent and reliable scientific evidence. Safe: measured in-app skill gains ("your times-tables speed went from 3.1 s to 1.4 s"). Not without RCT-grade evidence: "sharper at work", "better grades", "keeps your brain young", "improves memory/IQ" | https://www.ftc.gov/news-events/news/press-releases/2016/01/lumosity-pay-2-million-settle-ftc-deceptive-advertising-charges-its-brain-training-program |
| Ad platforms (e.g. Meta) restrict pairing a quantified result with a deadline in health and income ads, and restrict before/after claims. App Review has no specific outcome-plus-deadline rule but removes claims the app can't deliver or substantiate (2.3.1). Check each network's current policy | Platform ad policies |

## C§8 Scarcity, urgency, dark patterns and auto-renewal law

| Rule | Source |
|---|---|
| EU UCPD Annex I item 7: falsely claiming a product or terms are available only for a very limited time is unfair in all circumstances. Item 10: presenting rights consumers already have by law as a distinctive feature of your offer is banned | EU Directive 2005/29/EC, Annex I |
| UK DMCCA 2024 Schedule 20: para 7 bans falsely claiming a product or terms are available only for a "limited time" (wider than the UCPD's "very limited"); para 11 bans presenting legal rights as a distinctive feature; para 13 bans fake or concealed-incentivised reviews. The CMA can fine directly (since April 2025) and has acted against countdown timers that reset | https://www.legislation.gov.uk/ukpga/2024/13/schedule/20 |
| FTC staff report "Bringing Dark Patterns to Light" (2022) names false scarcity and fake countdowns. The FTC still enforces ROSCA and Section 5; the click-to-cancel rule was vacated on 2025-07-08 | https://www.ftc.gov/system/files/ftc_gov/pdf/P214800+Dark+Patterns+Report+9.14.2022+-+FINAL.pdf |
| California Automatic Renewal Law (Bus. & Prof. Code §17600 et seq., as amended by AB 2863, effective 2025-07-01): separate consent to auto-renewal, disclosure of renewal terms and cancellation before consent, notice of material price changes, annual reminders, online cancellation; covers free-to-paid trials. Fully applies to web checkout; how far it reaches store-billed offers is unsettled, so keep paywall disclosures complete | https://www.dwt.com/insights/2024/10/ab-2863-updates-california-automatic-renewal-law |
| EU Omnibus: a struck-through reference price must be the lowest price in the prior 30 days | EU Directive 2019/2161 |
| Apple 5.6: no manipulative practices; repeated misleading behaviour leads to removal | Guidelines |
| UK subscription contracts regime (DMCC Act), starting 2027-01-01: cooling-off after a free or discounted trial ends, and mandatory renewal reminders. How it applies to store-billed subscriptions is UNVERIFIED | https://cms.law/en/gbr/legal-updates/uk-subscription-contracts-the-government-publishes-the-missing-detail |

What's allowed: server-backed or hand-enforced counts, caps you genuinely enforce, end dates that never reset, seasonal events with real content, loss claims (such as a price lock) worded to match the store's real mechanics (C§4), and cancel-anytime stated as plain information rather than as your guarantee.

## C§9 Login, permissions, push

| Rule | Source |
|---|---|
| Apple 5.1.1(v): no login required unless the app has significant account-based features; if it has accounts, they must be deletable in the app | Guidelines |
| Apple 5.1.2(i): you may not require turning on push, location or tracking to use features or to receive compensation | Guidelines |
| Apple 4.5.4 and the subscriptions page: marketing push needs explicit opt-in with consent language and a clear opt-out, and must not contain sensitive personal information | https://developer.apple.com/app-store/subscriptions/ |
| Apple 4.10: you may not charge for built-in OS capabilities (push, camera) or Apple services (iCloud storage, Screen Time APIs), so reminders and widgets alone can't be the premium value | Guidelines |

## C§10 Kids, teens and age laws

| Rule | Consequence | Source |
|---|---|---|
| Apple 1.3 Kids Category: no links out and no purchases unless behind a parental gate; third-party analytics and ads only in narrow exceptions; the obligations continue even if the category is later deselected | Paywall goes behind a gate; Mixpanel and ad SDKs likely disallowed | Guidelines |
| Apple 5.1.4: for kids, ask for a birthdate or parental contact only to comply with law; the app must offer value regardless of age | Rejection or FTC exposure | Guidelines |
| Amended US COPPA Rule: effective 2025-06-23, compliance required by 2026-04-22. Disclosing children's data to third parties for targeted ads needs separate verifiable parental consent; retention limits are tighter | FTC enforcement | https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule |
| **Texas SB 2420 App Store Accountability Act (in force).** Fifth Circuit administrative stay of the injunction 2026-05-28, then a stay pending appeal in early June 2026. Supreme Court denied vacatur 2026-07-06 (No. 25A1390, https://www.supremecourt.gov/orders/courtorders/070626zr1_dc8f.pdf). Apple activated its Texas requirements on 2026-06-04. Developer duties: (1) age-rate the app and every IAP; (2) read the age category (under 13 / 13-15 / 16-17 / 18+) and consent status through the store API (Apple Declared Age Range API; Google Play Age Signals API); (3) rely on store parental consent for a minor's downloads and purchases, and handle consent that is pending or revoked; (4) notify the store of significant changes, such as adding IAP or ads, which re-triggers consent; (5) use the age data only for age enforcement, compliance and safety, and delete it after verification | Applies to every app with Texas users under 18, in any category. Enforced under the Texas DTPA (up to $10,000 per violation reported). Good-faith safe harbor if you rely on store signals. Cross-platform frameworks (Flutter, React Native) need a native bridge to these APIs | https://www.mofo.com/resources/insights/251111-texas-targets-app-stores-with-new-accountability-law |
| Utah (SB 142, amended by HB 498 on 2026-03-18): operative 2027-05-06; enforced only through a private right of action ($1,000 per violation or actual damages); safe harbor; adding IAP or ads counts as a significant change. Louisiana (HB 977 / Act 185 of 2026): 2027-07-01, Attorney General enforcement. Alabama: 2027-01-01 | One store-signal integration covers all of them. Dates have moved before | https://www.legal500.com/intelligence/united-states/privacy/key-developments-with-state-app-store-accountability-acts-as-texas-act-takes-effect |

Design rules for minors:
- Don't feed the store age band into quizzes, analytics or paywall targeting.
- When parental consent is pending, show a "waiting for parent" state and keep the free core usable.
- Don't route around the store's consent flow.
- Adult or parent positioning keeps an app out of the Kids Category and COPPA only if it is genuinely not child-directed. It never removes the state-act duties for teenage users.

## C§11 Payments outside IAP, web checkout and link-outs

| Rule | Source |
|---|---|
| Apple 3.1.3(d): real-time person-to-person services (e.g. 1:1 tutoring or coaching between two people) may be paid outside IAP. One-to-few and one-to-many services (group classes, cohorts, live group sessions) must use IAP. One customer account with several people on one call (a couple or a family) meeting one provider: classification UNVERIFIED; default to IAP or ask App Review | Guidelines |
| **Google Play has no person-to-person exemption.** Its Payments policy exceptions cover physical goods and services, peer-to-peer payments, auctions, tax-exempt donations, gambling and similar; live online coaching sold in an Android app needs Play Billing, or in the US an enrolled alternative-billing or external-content-links program (below) | https://support.google.com/googleplay/android-developer/answer/9858738 |
| Apple 3.1.3(b) Multiplatform services: access bought on the web or another platform may unlock features in the app if the same access is also offered as IAP | Guidelines |
| Apple 3.1.1: digital content and bonuses unlocked in-app must use IAP; purchased credits may not expire; restorable items need restore | Guidelines |
| **Apple US link-outs:** the guidelines (updated 2026-10-16) allow purchase buttons and links in US-storefront apps without an entitlement. Commission has been zero since the April 2025 contempt order. On 2025-12-11 the Ninth Circuit affirmed contempt but allowed a cost-based fee on remand. The Supreme Court granted cert on 2026-06-30 (No. 25-1311). Apple's August 2026 remand proffer proposed 15/10/5% tiers. No final rate is set. Outside the US, in-app links to web purchase are broadly not allowed without special entitlements | https://law.justia.com/cases/federal/appellate-courts/ca9/25-2935/25-2935-2025-12-11.html |
| **Google US:** Epic and Google withdrew their settlement and motion in mid-July 2026 (notice dated 2026-07-14), so the 2024 permanent injunction governs until 2027-11-01. Google may not require Play Billing for US users. Rival stores can be distributed through Play since 2026-07-22 | https://www.pocketgamer.biz/google-and-epic-withdraw-settlement-as-play-store-overhaul-moves-ahead/ ; timeline https://support.google.com/googleplay/android-developer/answer/15582165 |
| **Google US programs (enrollment required):** External content links (declaration form, onboarding, external-links API, Play Console enrollment). Fees apply within 24h of a link-out: 10% on auto-renewing subscriptions; 20% on other purchases for new installs (10% on the first $1M); plus $2.85 per non-game or $3.65 per game install for app-download links. Alternative billing: 10% on subscriptions, 20% (new installs) or 25% (existing installs) on other purchases, reported within 24h. Fees have applied since 2026-10-01; link-out download reporting is due by 2027-02-01. Whether Google may charge link-out fees was reported in July 2026 as still unresolved in court. Enrolled developers must provide support and refunds unless a purchase is clearly non-refundable | https://support.google.com/googleplay/android-developer/answer/16470497 ; fees https://support.google.com/googleplay/android-developer/answer/16497028 |

Implications:
- On iOS (US), web checkout currently saves the whole commission.
- On Android, a web subscription still pays 10% vs about 15% through Play Billing, so the saving is small after processor fees.
- Either way you lose store trials, Family Sharing and store-handled refunds, and you take on merchant-of-record duties (including California ARL, C§8).
- Linking out on Android without enrolling breaches Play policy.

## C§12 Delivery and packaging rules

| Rule | Source |
|---|---|
| Google: subscriptions must deliver sustained value; one-time benefits must be in-app products; you can't turn a subscription into a one-time offering after purchase | https://support.google.com/googleplay/android-developer/answer/9900533 |
| Apple Family Sharing (up to 5 family members) **can't be turned off once enabled**, so test before you commit. It covers iOS users in the same family group only | https://developer.apple.com/app-store/subscriptions/ |
| Sharing a purchase with other accounts (UNVERIFIED as a set): Apple Family Sharing as above; Google Play Family Library lets developers opt in to sharing some in-app items and subscriptions, so verify current scope for your product type; granting access to a linked account (a partner on another platform) through your own account system follows Apple 3.1.3(b) and Play's payments policy, so check both before promising cross-platform household access | Apple/Google docs |
| Apple 3.1.2(a): consumable credits may be bundled inside a subscription | Guidelines |
| Apple 3.1.2(a): users must get what they paid for without extra tasks (posting on social, uploading contacts, check-ins) | Guidelines |
| Apple 2.1: placeholder or "coming soon" features in the build get rejected; hiding them from review through remote config breaks 2.3.1 | Guidelines |
| Apple 3.2.2(v): apps may not arbitrarily restrict who can use them (e.g. by location or carrier), so price for regions instead of blocking them | Guidelines |
| Apple monthly-billed annual plan with a 12-month commitment (iOS 26.5 SDK, customers on OS 26.4+, selected markets). Google installment plans (BR, FR, IT, ES) and prepaid plans | Apple/Google docs |
| Apple Bundles and Suites, announced at WWDC26 for later in 2026 | Apple WWDC26 |

## C§13 Retention mechanics

| Item | Detail | Source |
|---|---|---|
| Apple | Billing grace period (3, 16 or 28 days) plus 60-day billing retry. Retention Messaging in the cancel flow (configured in App Store Connect or via a real-time API) can show a message, a plan switch or a promotional offer | https://developer.apple.com/videos/play/wwdc2026/309/ |
| Google | Grace period on by default (configurable; 0 is allowed, and Play still retries for at least a day); account hold on by default, lasting 60 days minus the grace period. Resubscribe after expiry is configurable per base plan and may not appear for subscriptions that expired long ago; the purchase token stays valid until 60 days after expiry. SUBSCRIPTION_CANCELED RTDN notifications trigger outreach | https://developer.android.com/google/play/billing/lifecycle/subscriptions |

## C§14 Benchmarks (2026 unless noted)

Coverage is strongest for Education and all-category medians. If your category is missing, say so in §7 and use the all-category row plus 5-10 live competitor prices (SKILL step 7.2); tag stand-ins [B].

| Metric | Value | Source |
|---|---|---|
| Education median prices | Yearly $44.99 (highest category); monthly $9.99 | https://www.revenuecat.com/state-of-subscription-apps-2026-education |
| Median prices, all categories | Weekly about $5.99 (most common $5); yearly $34.80; monthly $8-10 (inconsistent within the report) | RevenueCat SOSA |
| Median prices, Adapty | Weekly $7.48, monthly $12.99, annual $38.42. European apps charge 29-39% more than North American apps | Adapty |
| Download-to-trial (D30) | Business 9.1%, Health & Fitness 6.9%, Education 6.5%, Utilities 6.5%, Gaming 4.4% | RevenueCat SOSA |
| Trial-to-paid by geography | North America 34.2%, APAC 31.9%, Western Europe 29.7%, India/SEA 15.2% | RevenueCat SOSA |
| Year-1 LTV per payer by **user** geography | Europe $26.64; North America $26.07 (top quartile above $46); India/SEA $19.32. Use this cut for regional pricing | RevenueCat SOSA |
| Year-1 LTV by **developer HQ** | Global $23; North America $32; Western Europe $25; India/SEA $14; Education $22.82. Do not use for storefront pricing | RevenueCat SOSA |
| Revenue concentration | Top 10% of apps take 94.5%; median app earns $492/month; 59.3% of apps earned under $1k in total | Adapty |
| New subscription apps | 14,000+ per month | https://www.revenuecat.com/blog/growth/subscription-app-trends-benchmarks-2026 |
| Plan mix | About 42% monthly, 34% yearly; lifetime and other 4-18%; Education, Travel and Shopping 59-66% annual | RevenueCat SOSA |
| Weekly share of revenue | About 55.5% (Adapty sample); in RevenueCat data, weekly exceeds 30% of revenue only in Gaming | Adapty / RevenueCat |
| Price tier vs conversion | Download-to-trial: high tier 8.9% vs low 4.4%. Download-to-paid: 2.8% vs 1.4% (correlational) | RevenueCat SOSA |
| Monetisation mix | 63.5% subscriptions only; 23.2% add lifetime; 10.7% add consumables; 2.5% all three | RevenueCat SOSA |
| Price tests | Lift LTV 46% of the time and conversion 28% of the time | https://adapty.io/blog/markdown/how-to-personalize-onboarding-and-paywalls-in-your-mobile-app.md |
| Plans shown per paywall | Two plans dominate (41-60% by category); one plan 20-40%; three or more 6-27% | RevenueCat SOSA |
| Multi-page vs single-page onboarding paywall | 12.41% vs 9.07% (observational, 40M+ opens, Feb-May 2026) | https://superwall.com/blog/new-postmulti-page-onboarding-paywalls-convert-37-better-than-single-page-heres-why |
| Hard vs freemium, D35 download-to-paid | Hard median 10.7% (top quartile above 20%) vs freemium 2.1% (top quartile above 4.5%) | RevenueCat SOSA |
| Revenue per install, hard vs freemium | D14 $2.32 vs $0.27; D60 $3.09 vs $0.38 | RevenueCat SOSA |
| 1-year retention of yearly subscribers | Freemium 28% vs hard 27% | RevenueCat trends blog |
| Hard vs soft LTV per subscriber | Hard about 21% higher | Adapty |
| Refund rate by paywall type (2025) | Hard 5.8% vs freemium 3.4%; Education 4.86% | https://www.revenuecat.com/state-of-subscription-apps-2025/ |
| Onboarding paywall with trial | Install-to-paid 1.78%, the highest of any placement | Adapty blog |
| Trial starts on Day 0 | 89.4% (Adapty); by category: Business 89.9%, H&F 82.1%, Gaming 81.5%, Education 78.5%; under 5% start after Day 3. Users who miss the first session have about an 11% chance of ever starting a trial | Adapty / RevenueCat |
| Share of conversions on Day 0 | About 50.6% overall; Education 28.5%, with a Day-7 bump | RevenueCat Education |
| 3-day trial cancellations | 55.4% on Day 0 (about 84% by Day 1); 7-day trials 39.8%; 14-day 35.7%; 30-day 31.1% | RevenueCat SOSA |
| Trial-to-paid by trial length | 4 days or less 25.5%; 5-9 days 37.4%; 10-16 days 35.4%; 17-32 days 42.5%. Share of apps using 4 days or less rose to 46.5% | RevenueCat SOSA |
| Trial-to-paid by length, monthly vs annual | Monthly 39.6 / 45.9 / 46.6 / 43.7%; annual 24 / ~33 / ~43 / 44.6% | https://www.revenuecat.com/blog/growth/free-trial-length |
| First renewal by trial length (monthly) | No trial 49.5%; 4 days or less 54.2%; 5-9 days 62.8%; 10-16 days 72.0%; 17-32 days 77.5% | Same |
| Trial vs direct buyers | Trial subscribers retain 1.4-1.7x better | Adapty |
| Weekly vs annual conversion | Weekly converts 1.7-7.4x better | Adapty |
| Day-380 retention by plan | Annual with trial 19.9%; monthly with trial 14.2%; weekly 5.5% | Adapty |
| First renewal by category | Utilities 58.1%; Health & Fitness 30.3% | Adapty |
| Annual cancellations | 35% happen in month 1; about 72% cancel in year 1 | RevenueCat trends blog |
| Involuntary share of cancellations | Google Play 31% vs App Store 14% | RevenueCat trends blog |
| Apple Retention Messaging | Average save-rate uplift +1.4 points; with promotional offers +5.5 points (Apple's own claim) | https://developer.apple.com/videos/play/wwdc2026/309/ |
| Experimenting apps | About 40x more revenue (correlational) | Adapty |

## C§15 UNVERIFIED (don't present these as fact)

- Effect of scarcity, bonuses or naming on app conversion: no primary benchmark found.
- Effect of family or household plans on conversion or LTV: no primary benchmark found.
- Personalised onboarding lift (+8.5% trials, +17% paid, +22% ARPU): appears only in secondary summaries.
- The "How did you hear about us?" question lifting conversion about 10%: a single anecdote.
- Reverse trial taking freemium conversion from 0.4% to 4.5%: a contributor anecdote.
- 2026 refund rates (about 2.5% hard vs 2.9% freemium): third-party summary only.
- Impact of commitment and instalment billing: too new to have benchmarks.
- How the UK subscription regime applies to store-billed subscriptions; how far California's ARL reaches store-billed offers.
- A specific App Review rejection precedent for iOS money-back promises.
- What Google's legacy price cohort does when a subscriber cancels and later resubscribes.
- Google Play one-time-purchase fee below $1M (C§1).
- RevenueCat's current pricing tiers (C§1).
- Whether a couple or family on one call with one provider counts as person-to-person under Apple 3.1.3(d) (C§11).
- Cross-platform and household sharing of one purchase (C§12).
- Every row in C§16.
- Category benchmarks for Finance, Lifestyle, Productivity and Social: not collected in this file.

## C§16 Regulated and sensitive categories (finance, health, dating, location)

All rows UNVERIFIED until checked against the current source. Flag the app in SKILL step 0.8 and carry each applicable row into §13.

| Area | What to check |
|---|---|
| Google Play financial features | Play Console requires a financial features declaration for apps offering financial services (banking, loans, budgeting, crypto); some features need licences or extra documentation. Play Console Help: "Financial features declaration" |
| Apple 5.1.1(ix) | Apps that provide services in highly regulated fields (such as banking and financial services, healthcare, gambling, legal cannabis use and air travel), or that require sensitive user information, should be submitted by a legal entity that provides the services, not by an individual developer. If the sensitive-data flag is set, check whether the developer account must be an organisation; enrolling one (legal entity, D-U-N-S number) can take weeks, so start before launch. https://developer.apple.com/app-store/review/guidelines/#5.1.1 |
| Bank linking (aggregators) | Aggregator terms, security reviews and per-linked-account fees; this is variable cost (SKILL step 0.8) and a privacy-label category |
| Privacy labels and policy | Apple privacy nutrition labels and Google Data safety must declare financial info, health data, sensitive info or precise location if collected, including onboarding answers sent to analytics |
| FTC Safeguards Rule / GLBA | May apply to apps that handle consumers' financial data as a financial institution. https://www.ftc.gov/legal-library/browse/rules/safeguards-rule |
| Advice | No personalised investment advice without registration; credentialed services (financial, medical, legal) go to a licensed partner, never the founder |
| Health data | Apple HealthKit rules (no advertising use, no iCloud storage of health data) and health-claim substantiation (C§7) |
| Ad platforms | Financial services, dating and health are restricted ad categories on Meta and Google Ads; check certification requirements before paid acquisition |
| Misuse | Partner, family or location visibility can enable coercion or monitoring: private by default, opt-in sharing, a clean exit (SKILL step 11, F§17.5) |
