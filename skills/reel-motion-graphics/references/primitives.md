# Kit primitives

Every primitive below is already working inside `template/compositions/`. Copy the pattern from the named file instead of re-inventing it. Coordinates are frame px (1080×1920); all spacing stays on the 4px grid.

## Material and type (brand.css)

| Class / token | Use |
|---|---|
| `.glass` | Frosted warm panel: lit top edge, inner depth, drop shadow, 16px radius. Tween `--gloss` from −1 to 2 for one specular pass. Set `style="--gloss:-1"` on the element when a later tween uses `tl.to`. |
| `.headline` + `<em>` | Bodoni 60/64 with an italic gold accent. Tween `--sheen` from 0 to 100 on the `em` for a light sweep through the letters. |
| `.eyebrow` | Tracked caps label, 20/20, muted sand. |
| `--gold-sheen` | The gold gradient used by progress fills, rules, the accent text and stat numbers. |
| `--col-x` `--col-w` | The content column (172, 656 wide). Everything left-aligns to it, and the right edge 828 stays clear of the like/comment rail. |
| `--fold` | Where the presenter starts. Set it per footage with `scripts/solve-fold.py`. |

## Scene-level primitives

**Title card** (`title.html`). A credit eyebrow, two 128px display lines (the second italic with a sheen), a gold rule 8px tall, two thesis lines (32/40 body and 40/48 italic) and a mini glass diagram. The words rise out of a 14px blur with a 0.15s stagger. The whole root fades out over the last 0.5s of its host.

**Step headings** (`headings.html`). Data-driven: `STEPS = [[start, end, step, plain, accent], …]` in host-local seconds. The progress rail has one bar per step, filling with gold as its step first appears. Words rise from a blur with a 0.07s stagger, the accent catches a sheen 0.7s later, and each heading leaves with a 0.35s fade and a 10px lift. The final heading holds.

**Captions** (`captions.html`). Data-driven: `CAPS = [[in, out, line1 HTML, line2], …]` in global seconds. Line 1 is Bodoni italic 40/48 and may contain `<em>` for a sand accent. Line 2 is body 28/36 muted. Both sit in one caption band at y 812–904, and every caption lives on this single track.

**Stat cards** (`result.html`). Two glass cards side by side in a flex row with a 16px gap, padding 24px all round, sized to content. They flip in from rotationX −28 and z −160. Counters are a proxy object tweened with `tl.to(v, { x: to, onUpdate })` that writes `textContent`, so they are seek-safe. Never use `fromTo` on the same proxy twice.

## 3D diagram primitives (`diagram.html`)

The diagram is ONE continuous world for the whole explanation, so persistent things never jump between steps.

- **Lens and world.** `#dg-stage` has a static `perspective: 1100px`. `#dg-drift` holds a slow ±2° yaw drift, and `#dg-world` (preserve-3d) carries the camera pose. Tween the world's `rotationX`/`rotationY` for camera moves, such as a tilted establishing pose (16°, −28°) flattening to (7°, 0°). Never put `filter`, `opacity < 1`, `overflow` or `clip-path` on preserve-3d elements, because each one flattens the 3D.
- **Glass bars** (`.dg-bar.glass`): 52px tall, 24px side padding, a label left and a muted note right. Stack them with a 24px gap (attention at 372, router at 448).
- **Layer stack** (from the sparse-upcycling demo): rows of `[attention segment 476 | MLP segment flex]` with a 16px gap, 52 tall and 64 apart, flipping up from rotationX 60 with a 0.15s stagger. A `.dg-pick` ring marks the chosen segments. To zoom into one layer, fade the other rows and slide the chosen row to the top slot. Give every label `white-space: nowrap` and check that the segment width fits label, number and note.
- **Glass weight cards** (`.dg-card`): 72×168, padding 12, label 20/20, a 3×5 cell grid with 4px gaps. Cell brightness comes from seeded weights (`rng(seed)`), so copies are identical by construction. Rows use `SLOT = 80` (8px gaps), centred on x 500.
- **Slab → deck → row.** One card enters large (`scale: 1.5`, from z −320 and rotationY −40). Copies fade in behind it at z −40·i with an x offset of 10·i, as a deck. Then every card tweens to `x: (i − 3.5)·SLOT, z: −|i − 3.5|·16, rotationY: (i − 3.5)·−3, scale: 1`, which gives a gentle arc.
- **Gloss pass.** A staggered `--gloss` tween across a set of glass elements.
- **Verify scan.** A 4px light beam sweeps x across the row. Each card's `.dg-hit` ring flashes as the beam passes (yoyo 0.12s), timed by the card's x position.
- **Flow particles.** Tokens are drawn by ONE pure function of time (`drawTokens(t)`), called from a single 0 → duration `clock` tween with `ease: "none"` and `onUpdate`. It draws dots and SVG bezier trails, a router pulse and hit glows. Use this pattern for anything flowing (data, messages, gradients); never use `requestAnimationFrame`.
- **Divergence.** Per-card `backgroundColor` and `opacity` tweens on the cells to an identity colour and new weights, plus a `.dg-tint` edge ring, staggered 0.25s per card over 3.2s.
- **Notes under the diagram** (`.dg-note`): a centred caps line at y 760, 24/24. Enter with `scale 1.12 → 1`, never by tweening letter-spacing.
- **Backdrop recession.** When a result scene takes over, tween the diagram root's opacity to 0.1.

## Writing a new diagram

Map each beat of the script to one of these moves on the same world. Typical vocabulary:

| Script idea | Visual move |
|---|---|
| "X is made of Y" | glass bars and cards appearing in stack order |
| "copy / replicate / scale out" | slab → deck → row |
| "they're the same" | gloss pass + verify scan + note |
| "routing / selection / attention" | a new glass bar + flow particles to chosen targets with hit glows |
| "training / learning / drift" | divergence (colour + weights) |
| "the result / cost / numbers" | diagram recedes, stat cards count up |
| "compare A vs B" | two glass cards in a flex row, or two rows of cards at different z |

Keep about 4 cards visible per beat at most where you can. Hold each finished state at least 1s before the next move.

## Restyled from HyperFrames

Graphics adopted from the HyperFrames registry and restyled to the house rules. The restyled files live in `template/compositions/library/`. Add one entry per adoption: name · source link · what it shows · key parameters · which reel first used it.

_None yet. When a beat needs one, ask the user for a link (SKILL.md, step 3)._
