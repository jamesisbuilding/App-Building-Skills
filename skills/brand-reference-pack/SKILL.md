---
name: brand-reference-pack
description: Build or refresh a shortform brand reference pack for any app from its real surfaces — website, App Store listing and reviews, socials, the live app (driven end to end on the simulator) and its code tokens — plus a status check of the upstream foundations (ICP, voice of customer, brand voice). Produces the context that content formats and design decisions are made from, as markdown, tokens.json and a PDF. Use for "build a brand pack for <app>", "refresh the brand pack", "capture the site/app/socials for shortform", "/brand-reference-pack".
---

# Brand reference pack

**The pack is context, not content.** It records what the brand already is (audience, voice, visual language,
tokens, and the screens and copy each claim comes from) so that formats, scripts and design decisions can be made
*from* it later. No hooks, scripts or series in the pack. If a source suggests one, note the source and leave the
decision open.

**Where it sits:**
```
upstream (strategy) ──→ this skill (observed brand) ──→ downstream (formats, scripts, reels)
ICP · VOC · brand voice   what the surfaces say/show      script-to-reel, shader-lab
```
This skill doesn't establish ICP, voice of customer or brand voice. It finds the upstream artefacts, checks the
surfaces against them, and marks each one **verified / inferred / missing** (pack §0). Gaps go back upstream; don't
paper over them here.

**Files:**
- `template.md`: the pack's section structure.
- `scripts/`: generic capture and render helpers.
- `apps/<app>/`: one folder per app with its URLs, flow recipe, quirks, production rules and PDF layout.
  - **Read `apps/<app>/README.md` first.** For a new app, create it during intake.

Commands below are written relative to this skill folder (`.claude/skills/brand-reference-pack/`), and output paths are relative to wherever you run them. Run them from the project root and prefix `scripts/` with the skill path. `pack_pdf.py` resolves its config relative to the skill.

## 0. Intake (one AskUserQuestion round, new app only)
Collect:
- App name.
- Website URL.
- Social handles.
- App Store id and country (Play package id if relevant).
- How to run the app: simulator build, TestFlight, web app or emulator.
- Code repo path, if there is one.
- Existing brand, ICP or research docs.
- Which flow is the core one.
- What's off-limits in production.
- Output folder.

Write the answers to `apps/<app>/README.md`.

## 1. Foundations check (ICP, VOC, brand voice)
For each foundation, look for the upstream artefact: a wiki or docs folder, research decks, a brand book.
- **ICP:** a defined target customer backed by data or research. Note its confidence and its sample size.
- **Voice of customer:** customers' own words from interviews, reviews, support or community. Testimonials on the brand's own site count only as weak evidence: they're curated.
- **Brand voice:** a written voice guide or copy rules.

Record each one in the pack's §0 table. Through steps 2–5, check whether the live surfaces match the artefact. Mismatches go to Open decisions. If an artefact is missing, say so and name the upstream work that would fill it; don't invent the foundation from the surfaces.

## 2. Public surfaces (parallel where possible)
Every claim needs a file in `refs/`.

**Website:**
```bash
node scripts/site.mjs <url> <brand>/refs/web
```
This saves full and hero screenshots for desktop and mobile, plus `site-styles.json` with fonts (including real names behind font-host ids), colours, images, links and the page text. Slice the full-page shot into about 4 parts to read it.

**App Store:**
```bash
node scripts/store.mjs <id> <brand>/refs/store [country]
```
This saves the listing (the official positioning), the store screenshots, and reviews as raw VOC material.

**Socials** (in the built-in browser):
- Decline optional cookies.
- Grid: collect each post's image `src` and `alt`, draw them onto a canvas, replace the page with it and screenshot.
- Captions: same-origin fetch of each post page → `og:description`.
- Logged out, you only get about 12 posts. Say so, and if the reels matter, ask the user to log in or export.
- If you get the reels, note their pace, caption style and audio.
- Write everything to `refs/<platform>/`.

**Existing docs:** use an Explore subagent to synthesise audience, promise, terminology, voice rules and claims, with file citations.

## 3. Code tokens (if there's a repo)
Use an Explore subagent to find the theme for whatever framework the app uses:
- Flutter `ThemeData` and colour constants
- Tailwind config
- CSS variables
- iOS asset catalogs
- Android `colors.xml`

Also cover fonts, radii, motion conventions, shaders, logo files and notable UI copy. Spot-check the hexes yourself. Write `tokens.json` with colour roles, the type scale (scaled to 1080×1920), shape, motion and canvas.

**In-app copy:** extract every user-facing string from the UI code, verbatim with file:line, for the persona brain (step 7):
```bash
python3 scripts/app_copy.py <src root> <persona>/raw/app-copy/app-copy-<date>.md <ui dirs/files…>
```
(Flutter: `app/lib` with `pages widgets constants models enums main.dart`; `--ext=.tsx` etc. for other stacks.) It
filters logs, keys and ids; still skim the output for anything secret before it lands in the brain.

## 4. Live app walk
The richest source: this is where the product's actual visual and verbal grammar shows up.
- **Consent first:** state exactly what the run writes to production (account, assessment answers, generated reports, completions) and get a yes. The user does every sign-up and login. Never type credentials, never subscribe, never message an AI coach.
- **Watch and record:** attach the simulator panel (`mcp__Claude_Code_iOS_Simulator__control attach`).
  - Start `xcrun simctl io <UDID> recordVideo --codec=h264 --force <file>` in the background.
  - **Stop it during sign-in and start a new one after**, so nothing needs trimming.
  - Stop with `pkill -INT -f recordVideo`.
- **Drive by accessibility labels, not coordinates:** `UDID=… OUT=<brand>/refs/app scripts/ui.sh tree|shot|label|tap|swipe|hold`.
  - Take a shot of every new screen, named after its heading.
  - Wait for animations and CMS copy to settle before shooting; if a line hasn't rendered, it's "not captured".
  - Build a contact sheet per stage (PIL, a few lines) and read that, not each PNG.
- **Follow the app's recipe** in `apps/<app>/README.md`. Add any new quirks you hit back into it.
- **Audio:** the simulator recording has none. If the app has voice or audio, ask the user for a source file.
- **Afterwards:**
  - Renumber the screenshots in capture order.
  - Build `refs/app-flow-sheet.jpg`.
  - Compress the recordings: `scale=540:-2,fps=30,crf 26`.

## 5. Write the pack
Fill `template.md` into `<brand>/README.md`.
- Quote only what you saw.
- Where surfaces disagree, the newest live surface is the working default and the disagreement goes in Open decisions.
- §0 comes from step 1.

## 6. Verify
Hand a fresh subagent the README and the `refs/` folder, not your conclusions. Ask it to check every quoted line, hex and claim against a file, and to list anything with no source. Fix or mark each item before hand-back.

## 7. Output
- **PDF:** write `apps/<app>/pdf.json` (copy the GetAhead one: cover, font, accent, palette groups pointing at `tokens.json`, specimen lines, screenshot pages). Then run:
  ```bash
  python3 scripts/pack_pdf.py apps/<app>/pdf.json
  ```
  Check the result as a `pdftoppm -r 40` contact sheet.
- **Docs:** if the project has a wiki or docs, file the pack there following its own conventions (page, index, log, contradiction flags on the pages it supersedes).
- **Persona brain:** if the project has one (e.g. `persona/`, the brand-as-a-person brain that script generation
  speaks from), copy the app walk's captures into its `raw/app-run-<date>/` and the in-app copy into
  `raw/app-copy/` (with the user's yes: `raw/` is theirs), then run the brain's own ingest workflow (its `CLAUDE.md`):
  source pages, concept pages, card rebuild with verbatim app lines. The pack records what the brand looks like;
  the brain records how it talks — scripts draw on the brain.
- **Send:** the PDF and README, with SendUserFile.
- **Report:**
  - what was written to production
  - what wasn't captured
  - the foundations status
  - the open decisions
