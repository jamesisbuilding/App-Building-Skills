# App Building Skills

Claude skills, plugins and MCP servers for building apps in the age of AI, from idea selection to deployed and scaling. Ordered by the 16 stages of my **Zero to Shipped** app SOP, so each stage lists the skills that run it.

My own skills live in [`skills/`](skills/). Everything else links out. For design resources see [UX and UI Resources](https://github.com/jamesisbuilding/UX-and-UI-Resources).

**Key:** **(mine)** = a skill in this repo · ✅ = used to ship [7 Minute Math](#proven-on-7-minute-math) · **gap** = nothing covers this stage yet, so it's manual or a skill to build.

## Install my skills

```bash
git clone https://github.com/jamesisbuilding/App-Building-Skills.git
cp -R App-Building-Skills/skills/* ~/.claude/skills/
```

Each skill folder has a `SKILL.md`; most also have a `README.md` with setup notes.

---

## The pipeline

| # | Stage | Track | Skills |
| --- | --- | --- | --- |
| 00 | [Foundations](#00-foundations) | Strategy | deep-work, ponytail, i-have-adhd, eli5 |
| 01 | [Ideation](#01-ideation) | Strategy | app-arbitrage, app-keyword-research |
| 02 | [Market analysis](#02-market-analysis) | Strategy | app-arbitrage, app-keyword-research, competitor analysis, Replica |
| 03 | [Customer avatar](#03-customer-avatar-icp--voc) | Customer | **gap** |
| 04 | [Validation](#04-validation) | Customer | replica-launch (landing page) |
| 05 | [Offer & business model](#05-offer--business-model) | Revenue | app-offer, Paywall Gallery |
| 06 | [Branding](#06-branding) | Marketing | appicon-creator, replica-brand |
| 07 | [Product & UX design](#07-product--ux-design) | Product | grill-me, ASD-STE100, Appllama, Mobbin, diagrams |
| 08 | [App development](#08-app-development) | Product | create-app, app-set-up-infra, VGV, REA |
| 09 | [Pre-launch & go-to-market](#09-pre-launch--go-to-market) | Marketing | brag, Hyperframes, Remotion, Instagram |
| 10 | [Launch](#10-launch) | Marketing | new-app-info, Mobile App Ship |
| 11 | [Acquisition](#11-acquisition) | Marketing | Instagram agent |
| 12 | [Activation & retention](#12-activation--retention) | Customer | **gap** |
| 13 | [Monetisation optimisation](#13-monetisation-optimisation) | Revenue | app-offer (shipped mode) |
| 14 | [Measure & iterate](#14-measure--iterate) | Strategy | after-action-report, ig-audit |
| 15 | [Scale](#15-scale) | Strategy | **gap** |

---

## 00 Foundations

How you work with Claude before any app exists.

- **[deep-work](skills/deep-work/) (mine) ✅** Timekeeper for a 90-minute build block: Orient, Build, Verify, Harden, Close, with a parking lot and a close-out log.
- **[Ponytail](https://github.com/dietrichgebert/ponytail) ✅** Write code like a seasoned pro: the smallest change that fully solves the task.
- **[I have ADHD](https://github.com/ayghri/i-have-adhd)** Clear, concise responses with a clear next step.
- **[ELI5](https://github.com/dreambigou/eli5)** Explain anything at varying levels of complexity.
- **[Understand Anything](https://github.com/Egonex-AI/Understand-Anything)** Break anything down so you internalise it instead of being an AI zombie.

## 01 Ideation

- **[app-arbitrage](skills/app-arbitrage/) (mine)** Paste a successful App Store app; get every review Apple exposes (36 storefronts), coded by subagents, tangential markets checked, and one scored rebuild tweak. Seeds `features.csv`. This is "rip an app idea and find the opportunity".
- **[app-keyword-research](skills/app-keyword-research/) (mine) ✅** Turn an idea into search phrases and measure demand (App Store autocomplete) against competition (current top 10). Compare ideas before building.

## 02 Market analysis

- **app-arbitrage** and **app-keyword-research** (above).
- **[Mobile Competitor Analysis](https://mcpmarket.com/tools/skills/mobile-app-competitor-analysis-1)** Feature gaps from competitor reviews and pain points, keywords, and a screenshot audit.
- **[Replica](https://github.com/Jakeschincariol/replica-skill)** `replica-entrepreneur` ranks what competitors' users hate and miss; `replica-recon` tears down screens, flows and features.
- **RankPilot MCP ✅** Keyword tracking per market: volume, difficulty, competitor keywords.

## 03 Customer avatar (ICP + VOC)

- **gap.** No skill for ICP, interviews or voice-of-customer mining. Start with the verbatim quotes `app-arbitrage` and `replica-entrepreneur` collect.

## 04 Validation

- **[Replica](https://github.com/Jakeschincariol/replica-skill)** `replica-launch`, landing page only, to smoke-test the angle.
- **gap:** interviews, fake doors, pre-sales.

## 05 Offer & business model

- **[app-offer](skills/app-offer/) (mine) ✅** Alex Hormozi's $100M Offers method adapted to the App Store: value equation, value stack, pricing tiers, guarantee, naming, paywall per placement, onboarding fast win, test plan. Works for new ideas and shipped apps.
- **[Paywall Gallery](https://github.com/paywallpro/paywall-gallery)** 1,600+ iOS paywalls as markdown with pricing. Clone it and let `app-offer` filter by category.
- **[Appllama](https://github.com/Appllama/appllama-skills)** `appllama-usage` for paywall and onboarding flow research across top-grossing apps.

## 06 Branding

- **[appicon-creator](skills/appicon-creator/) (mine) ✅** App icons to Apple's Human Interface Guidelines: one strong symbol, audit, production export.
- **[Replica](https://github.com/Jakeschincariol/replica-skill)** `replica-brand` for names, trademark, domain and handle checks, palette and voice.

## 07 Product & UX design

- **[Grill me](https://www.aihero.dev/skills-grill-me) ✅** Align Claude to your intent and walk every edge case before execution.
- **[ASD-STE100](https://github.com/danyuchn/asd-ste100-skill)** Write requirements in non-ambiguous Simplified Technical English.
- **[Appllama](https://appllama.io/)** Study winning apps and build to their quality bar (`appllama-usage`, `appllama-app-design-skill`, Appllama MCP).
- **[Mobbin](https://mobbin.com/discover/apps/ios/latest)** Real app screens and flows for inspiration.
- **[Diagrams](https://github.com/cathrynlavery/diagram-design)** Diagrams for flows and architecture.
- **[Replica](https://github.com/Jakeschincariol/replica-skill)** `replica-design` for design tokens and a contrast checker.
- More: [UX and UI Resources](https://github.com/jamesisbuilding/UX-and-UI-Resources).

## 08 App development

- **[create-app](skills/create-app/) (mine) ✅** Scaffold a Flutter app with the house structure: four layers (data client → repository → Cubit → view), localization, very_good_analysis, tests mirroring `lib/`, a `CLAUDE.md`.
- **[app-set-up-infra](skills/app-set-up-infra/) (mine) ✅** Branches, a private GitHub repo and GitHub Actions CI that uploads every push to `main` to TestFlight, then watches CI until green.
- **[VGV Flutter plugin](https://github.com/VeryGoodOpenSource/vgv-ai-flutter-plugin)** Flutter best practices from Very Good Ventures (`create-app` builds on it).
- **[Reverse Engineer Anything (REA)](https://github.com/morluto/rea) ✅** See what local software does under the hood and take its best practices.
- **[Replica](https://github.com/Jakeschincariol/replica-skill)** `replica-architect`, `replica-test`, `replica-diff` for method and QA. They default to Expo/Next.js, so tell them the stack is Flutter.

## 09 Pre-launch & go-to-market

- **[Brag](https://github.com/latent-spaces/brag) ✅** Launch videos for your software, built on Hyperframes (`brag-slim` is the one-file version).
- **[Hyperframes](https://github.com/heygen-com/hyperframes) ✅** HTML-based video compositions and rendering.
- **[Remotion](https://www.remotion.dev/)** Video in React.
- **[Instagram Agent](https://github.com/Jakeschincariol/instagram-agent-skill)** `ig-plan`, `ig-profile`, `ig-reel`, `ig-carousel`, `ig-story`.

## 10 Launch

- **[new-app-info](skills/new-app-info/) (mine) ✅** Answers App Review's "we need additional information" with all six required items, built from the app's own code, plus Apple's common-issue checks.
- **[Mobile App Ship](https://mcpmarket.com/tools/skills/mobile-app-ship)** Guides the app to a submittable state.
- **[Replica](https://github.com/Jakeschincariol/replica-skill)** `replica-launch` listing lint, `replica-deploy` preflight checklist.

## 11 Acquisition

- **[Instagram Agent](https://github.com/Jakeschincariol/instagram-agent-skill)** `ig-viral`, `ig-repurpose`, `ig-comment`, `ig-dm`, `ig-reply`. They draft, you send.

## 12 Activation & retention

- **gap.** No skill yet.

## 13 Monetisation optimisation

- **app-offer (mine)** in shipped-app mode: reads the code and gives a before/after offer.
- **[Paywall Gallery](https://github.com/paywallpro/paywall-gallery)** What converts and what to test.
- **gap:** experiment analysis.

## 14 Measure & iterate

- **[After Action Report](https://github.com/rampstackco/claude-skills/blob/main/skills/after-action-report/SKILL.md)** Structured retro after a build or launch.
- **[Developer Growth Analysis](https://github.com/ComposioHQ/awesome-claude-skills/tree/master/developer-growth-analysis)** Review your own sessions to find where you can improve.
- **[Instagram Agent](https://github.com/Jakeschincariol/instagram-agent-skill)** `ig-audit` for social.
- **gap:** metrics digest, experiment log.

## 15 Scale

- **gap.** No skill yet.

---

## Proven on 7 Minute Math

The skills used to take 7 Minute Math from idea to the App Store, in order:

`app-keyword-research` → `app-offer` → `appicon-creator` → `create-app` → `app-set-up-infra` → `new-app-info` → `brag` / `hyperframes`, with `deep-work`, `ponytail`, `grill-me` and REA throughout, and the RankPilot and RevenueCat MCPs. `app-arbitrage` came after, for the next app.

## Finding more skills

- **[MCP Market](https://mcpmarket.com/)** Directory of skills and MCP servers.
- **[Agentic Design](https://agentic-design.ai/)** Patterns for agentic systems.

## Adding a skill (for me)

1. Build it in `~/.claude/skills/<name>/` (or symlink it there).
2. Add `<name>` to `SKILLS` in [`sync.sh`](sync.sh) and to its stage above.
3. Run `./sync.sh`. It copies every listed skill, strips private files (`examples/`, the Hormozi transcript), commits and pushes.
