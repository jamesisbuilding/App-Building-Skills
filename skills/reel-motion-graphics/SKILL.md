---
name: reel-motion-graphics
description: Turn a script or concept into an on-brand 9:16 explainer reel (luxury tech, warm sand on near-black, glassmorphism, CSS 3D, Bodoni + Instrument Sans) built in HyperFrames, with the animation above the fold and the presenter's talking head below. Use when the user gives a script, transcript, paper summary or concept and asks for a reel, motion graphics, an animated explainer or "the same style as the upcycling reel". Produces a HyperFrames project, a rendered MP4 and a live artifact player.
---

# Reel motion graphics

This skill makes reels in the house style first built for "Upcycling in 30 Seconds". `template/` is that reel as a working HyperFrames project, so a fresh copy renders correctly before you change anything. Your job is to replace its content with the new script's while keeping every rule below.

Load `/hyperframes-core` for the composition contract before writing composition HTML. Load `/hyperframes-animation` only if you need a motion pattern not in `references/primitives.md`.

## 1. Read the script and plan the beats

Gather or infer the following, and ask only for what changes the film:
- **The script or concept.** Required.
- **Presenter footage** (MP4) or a still. Without one, keep the template's placeholder still.
- **Source credit** for the title eyebrow, e.g. `ICLR 2023 · Author et al.`.
- **Target length.** Default 30s; 20–60s works.

Break the script into: a **title card** (about 4s), **2–5 steps** (4.5–6s each), and an optional **result/closer** (about 5.5s). For each step write:
- a **heading** as plain words plus a 1–2 word italic accent ("Copy the MLP *eight times*"), at most about 22 characters so it fits 656px at 60px;
- a **caption**: line 1 is one sentence of at most about 34 characters (Bodoni italic 40px), and line 2 is a supporting sentence of at most about 40 characters;
- the **diagram move** from the primitives vocabulary (`references/primitives.md` → "Writing a new diagram").

Pace about 2.5 spoken words per second if the captions mirror narration. Write the plan to `STORYBOARD.md` in the project (beat, time range, heading, caption, visual move), show it to the user, and build once they approve. A short script the user has already approved can go straight to the build.

## 2. Scaffold

This skill lives in the Reel Creator project (`.claude/skills/reel-motion-graphics/`). Run commands from the project root, and put every new reel in `reels/<slug>/`. Script paths below such as `scripts/solve-fold.py` are relative to this skill's folder.

```bash
.claude/skills/reel-motion-graphics/scripts/new-reel.sh reels/<slug> [presenter.jpg|.mp4]
```

For presenter video, replace the `<img id="presenter">` in `index.html` with:
`<video id="presenter" class="clip" src="assets/presenter.mp4" data-start="0" data-duration="<D>" data-has-audio="true" playsinline></video>`
The `#presenter` CSS (cover, 20% anchor, below `--fold`) applies unchanged.

## 3. Build: edit data first, then write the diagram

| File | What to change |
|---|---|
| `index.html` | Root and host `data-start`/`data-duration` to match the plan. Hosts: bg (whole), title (0–4), headings and diagram (4–end), result (its window), captions (whole), presenter (whole). |
| `compositions/title.html` | Eyebrow credit, the two display lines, the two thesis lines, and the mini diagram if the idea isn't "1 → many". |
| `compositions/headings.html` | Only the `STEPS` array (host-local seconds). Bars and "Step n of N" are derived from it. |
| `compositions/captions.html` | Only the `CAPS` array (global seconds). Enter each about 0.35s after its step starts and leave at the step's end. |
| `compositions/diagram.html` | Rewrite the world for the new subject, using the primitives. Keep the lens/world/drift structure, the token-clock pattern and the backdrop recession. |
| `compositions/result.html` | Stat labels, values, counters and meta lines, or delete the host if the script has no numbers. |
| `compositions/bg.html` | Usually unchanged. Scale its yoyo repeats so they finish at the root duration. |

### When the library has no fitting graphic: ask for a HyperFrames link

The library is `references/primitives.md`. When a beat needs a visual that no primitive covers (a chart type, map, timeline, comparison or anything else not listed), do not improvise one from scratch. Pause and ask the user for a link:

> "Beat 3 ('revenue tripled since 2021') needs a growth chart and the library doesn't have one. Can you send a HyperFrames catalog link for a graphic you like? I'll restyle it to our brand."

To help them pick, you may list 2–4 candidates from `npx --yes hyperframes@0.8.149 catalog "<keyword>"`, but let the user choose. Keep building the other beats while you wait, and leave a labelled placeholder in the gap.

When the link arrives:
1. **Install it.** The registry item name is the last path segment of the catalog link. Run `npx --yes hyperframes@0.8.149 add <name> --no-clipboard --json` from the project. For a link that isn't from the registry, read the page or source and rebuild it.
2. **Restyle it to the house rules:**
   - swap the colours for brand tokens and the panels for `.glass`;
   - use Bodoni and Instrument Sans with the opsz-18 files;
   - put every spacing value on the 4px grid;
   - fit it to the content column and zones;
   - add the sheen, gloss and drift accents;
   - remove anything off-brand, such as flat bright fills, other fonts or drop-shadow styles.
3. **Wire it in** as a sub-composition host on the graphics track, or fold its motion into `diagram.html` when it has to share the continuous world. Then check, snapshot and fix as usual.
4. **Add it to the library.** Append an entry to `references/primitives.md` under "Restyled from HyperFrames": the name, the source link, what it shows, and its key parameters. Copy the restyled file into `template/compositions/library/` so the next reel can reuse it without asking again.

## 4. House rules (every reel, no exceptions)

1. **Fold equidistant.** The fold sits halfway between the lowest animation content (caption bottom, about y 900) and the top of the presenter's head. Solve it with `scripts/solve-fold.py <presenter still or a frame> 900` and set `--fold` in `brand.css` (a multiple of 4). Verify with `scripts/measure-fold.py <snapshot> <fold>`. With video, check a frame where the head is highest.
2. **4px grid.** Every padding, gap, offset, size and line-height is a multiple of 4. Containers pad evenly and size to their content; never give a card a fixed height. Run `scripts/audit-grid.sh <project>`; the only allowed leftovers are hairline borders, glow radii and tween motion offsets.
3. **Sturdy serif.** Use only the `*-opsz18.woff2` Bodoni files in `fonts/`. The variable font's automatic optical size picks hairline display cuts that disappear after H.264 and phone downscaling. Never switch back to the variable file or Google's 6..96 range.
4. **Zones.** App bar 0–175 (keep clear), animation 192–780, caption band 812–904, presenter below `--fold`, content column x 172–828 (clear of the right rail). Captions live on one track only.
5. **One continuous diagram world.** Elements that persist across steps live in `diagram.html` and move. They never re-enter in a new scene file.
6. **Determinism.** Use only paused GSAP timelines registered on `window.__timelines["<id>"]`. Use seeded `rng()` or `hh()` instead of `Math.random`, and no `requestAnimationFrame`, clocks or network. Animated counters and particles are pure functions of a proxy tween's value.
7. **Lint-safe authoring.**
   - Target a sub-composition's own root with `document.querySelector('[data-composition-id="<id>"]:not([data-composition-src])')`, never `#root` (several roots share that id once assembled).
   - Prefix element ids with the composition (`dg-`, `hd-`, `rs-`, `ti-`).
   - Use one `fromTo` per element-property pair, then `to`.
   - Never tween `letterSpacing`, `width`, `height`, `top` or `left`; use transforms and opacity.
   - Stagger lone labels so they don't overlap at rest.
8. **Look.** Near-black warm background with drifting light and grain; `.glass` for every panel; gold sheen on accents; small camera drift on every hold; hold each finished state at least 1s.

## 5. Verify, then deliver

Run these from the project directory:

```bash
npx --yes hyperframes@0.8.149 check
npx --yes hyperframes@0.8.149 snapshot --at <the midpoint of every beat>
```

- `check` must pass with 0 errors. Review any warnings.
- Look at the contact sheet. Crop and zoom any dense frame: watch for overlaps, clipped text, tokens landing off target and uneven padding.
- Run `measure-fold.py` and `audit-grid.sh`, and fix anything they flag.
- Render with `npx --yes hyperframes@0.8.149 render`; the result goes to `renders/`. Make a share copy under 30 MB for phone viewing:
  `ffmpeg -i renders/<file>.mp4 -c:v libx264 -crf 23 -preset slow -pix_fmt yuv420p -movflags +faststart renders/<slug>-share.mp4`
- Live player: from the project root run `node viewer/build.mjs`. It rebuilds every reel's live player (`reel/` plus each `reels/<slug>/`) and writes the carousel `viewer/index.html`, with one copy per reel in `viewer/reels/`. Publish `viewer/index.html` to the reel library artifact https://claude.ai/artifact/Joet84qdr6Kb47vYZzc8YR, passing every `viewer/reels/*.html` in `files`. The user prefers the live HTML player over an embedded video. For a single reel on its own, `node build-preview.mjs` in its folder writes `dist/preview.html`.
- Report the runtime, what was checked (frames, fold gaps, audit), and anything not yet verified.

## Reference

- `references/primitives.md`: every visual building block, with the file that implements it.
- `template/`: the complete Upcycling reel. It is the quality bar; compare new work against it.
