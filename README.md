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
| 01 | [Ideation](#01-ideation) | Strategy | app-arbitrage, app-keyword-research, grill-me |
| 02 | [Market analysis](#02-market-analysis) | Strategy | app-arbitrage, app-keyword-research, competitor analysis, Replica |
| 03 | [Customer avatar](#03-customer-avatar-icp--voc) | Customer | **gap** |
| 04 | [Validation](#04-validation) | Customer | replica-launch (landing page) |
| 05 | [Offer & business model](#05-offer--business-model) | Revenue | app-offer, Paywall Gallery |
| 06 | [Branding](#06-branding) | Marketing | appicon-creator, brand-reference-pack, replica-brand |
| 07 | [Product & UX design](#07-product--ux-design) | Product | ASD-STE100, Appllama, Mobbin, diagrams |
| 08 | [App development](#08-app-development) | Product | create-app, app-set-up-infra, VGV, REA |
| 09 | [Pre-launch & go-to-market](#09-pre-launch--go-to-market) | Marketing | brag, reel-script, reel-motion-graphics, Hyperframes, Remotion, Instagram |
| 10 | [Launch](#10-launch) | Marketing | new-app-info, Mobile App Ship |
| 11 | [Acquisition](#11-acquisition) | Marketing | reel-study, Instagram agent |
| 12 | [Activation & retention](#12-activation--retention) | Customer | **gap** |
| 13 | [Monetisation optimisation](#13-monetisation-optimisation) | Revenue | app-offer (shipped mode) |
| 14 | [Measure & iterate](#14-measure--iterate) | Strategy | after-action-report, ig-audit |
| 15 | [Scale](#15-scale) | Strategy | **gap** |
| — | [Expert brains](#expert-brains) | All | channel-brain, cb-ingest, talk-to |

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

- **[Grill me](https://www.aihero.dev/skills-grill-me) ✅** Interviews you in rounds about a loose idea until you can commit to it. Writes no files; you have to push back, not just agree.

## 02 Market analysis

- **app-arbitrage** and **app-keyword-research** (above).
- **[Mobile Competitor Analysis](https://mcpmarket.com/tools/skills/mobile-app-competitor-analysis-1)** ASO teardown of rival apps: metadata, review sentiment, screenshots and icons, keywords they rank for that you don't, monetisation and update cadence.
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
- **[brand-reference-pack](skills/brand-reference-pack/) (mine)** Builds a brand pack for any app from its real surfaces (website, App Store listing and reviews, socials, the live app driven on the simulator, code tokens) and checks the ICP, VOC and brand voice it depends on. Outputs markdown, `tokens.json` and a PDF that content and design decisions start from.
- **[Replica](https://github.com/Jakeschincariol/replica-skill)** `replica-brand` for names, trademark, domain and handle checks, palette and voice.

## 07 Product & UX design

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
- **[reel-script](skills/reel-script/) (mine)** Writes the spoken script for a 20–60s explainer reel: question hook, a real story from the presenter, every concept explained simply (via ELI5), timed into beats for recording.
- **[reel-motion-graphics](skills/reel-motion-graphics/) (mine)** Turns that script into a 9:16 explainer reel in HyperFrames, animation above the fold and talking head below. Outputs the project, a rendered MP4 and a live player. The look is my house style; swap `template/brand.css` for yours.
- **[Hyperframes](https://github.com/heygen-com/hyperframes) ✅** HTML-based video compositions and rendering.
- **[Remotion](https://www.remotion.dev/)** Video in React.
- **[Instagram Agent](https://github.com/Jakeschincariol/instagram-agent-skill)** `ig-plan`, `ig-profile`, `ig-reel`, `ig-carousel`, `ig-story`.

## 10 Launch

- **[new-app-info](skills/new-app-info/) (mine) ✅** Answers App Review's "we need additional information" with all six required items, built from the app's own code, plus Apple's common-issue checks.
- **[Mobile App Ship](https://mcpmarket.com/tools/skills/mobile-app-ship)** Ships a Flutter + Firebase app: preflight, build and signing checks, RevenueCat purchases and ASO, then phased TestFlight, App Store and Google Play submissions, pausing for your approval before any store change.
- **[Replica](https://github.com/Jakeschincariol/replica-skill)** `replica-launch` listing lint, `replica-deploy` preflight checklist.

## 11 Acquisition

- **[reel-study](skills/channel-brain/.claude/skills/reel-study/) (mine)** Rips reels, TikToks and Shorts into study cards (transcript, caption, keyframes in a hook/story/visuals template) to build a swipe file of what stops the scroll. Part of channel-brain.
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

## Expert brains

The SOP's councils are LLM wikis built from each expert's material. These build and run them.

- **[channel-brain](skills/channel-brain/) (mine)** Paste a YouTube channel or playlist; every video is ripped, transcribed and ingested into its own wiki brain. Run it from the folder root; brains land in `brains/`.
- **cb-ingest (mine)** Adds anything to an existing brain: a video, a channel, or local PDFs, docs and folders.
- **talk-to (mine)** Builds personas from a brain and lets you talk to them directly ("get X's take on this"). This is how you run a council room.

---

## Proven on 7 Minute Math

The skills used to take 7 Minute Math from idea to the App Store, in order:

`app-keyword-research` → `app-offer` → `appicon-creator` → `create-app` → `app-set-up-infra` → `new-app-info` → `brag` / `hyperframes`, with `deep-work`, `ponytail`, `grill-me` and REA throughout, and the RankPilot and RevenueCat MCPs. `app-arbitrage` came after, for the next app.

## Finding more skills

- **[MCP Market](https://mcpmarket.com/)** Directory of skills and MCP servers.
- **[Agentic Design](https://agentic-design.ai/)** Patterns for agentic systems.

## Adding a skill (for me)

1. Build it in `~/.claude/skills/<name>/` (or symlink it there).
2. Add `"name|source folder|extra excludes"` to `SKILLS` in [`sync.sh`](sync.sh) (the source can be anywhere, e.g. a project's `.claude/skills/<name>`), and add the skill to its stage above.
3. Run `./sync.sh`. It copies every listed skill, strips private files (`examples/`, the Hormozi transcript), commits and pushes.
