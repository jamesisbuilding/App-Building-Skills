# app-offer

A Claude Code skill that designs one "Grand Slam Offer" for an app idea, new or already shipped. It runs Alex Hormozi's *$100M Offers* method, adapted to App Store and Google Play rules: market and niche, value equation, value stack, pricing and tiers, scarcity, urgency, bonuses, guarantee, naming, paywall placements, onboarding, test plan and ship plan.

## Use it

In Claude Code, type `/app-offer` or say "run app-offer on <idea>". Inside an existing app's repo, it reads the pricing, paywall, onboarding and notes first, and writes a before/after. Output goes to `offer/grand-slam-offer.md`, or to `./<app-slug>-grand-slam-offer.md` for a new idea.

## Install

This folder is the skill. It's installed by a link: `~/.claude/skills/app-offer` points here. To install it on another machine:

```bash
ln -s ~/Desktop/app-offer ~/.claude/skills/app-offer
```

## What's here

| Path | What it is |
|---|---|
| `SKILL.md` | The 12-step procedure and the output template |
| `reference/frameworks.md` | Every framework from the book, applied to apps, with rubrics, examples and what doesn't carry over |
| `reference/app-store-constraints.md` | Store policies and subscription benchmarks with sources and an "as of" date. Re-verify before shipping. |

Built 2026-10-28 from the transcript, with every extraction, draft, critique and revision judged to F1 = 1.
