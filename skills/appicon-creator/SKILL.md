---
name: app-icon-design
description: Create, revise, and audit app icons using Apple's Human Interface Guidelines, with a clear visual identity and production-ready deliverables.
version: 1.0
verified: 2026-10-24
---

# App Icon Design Skill

## Trigger
Use for any new app icon, icon redesign, icon critique, or Apple app-icon export request. Check Apple's current design and technical documentation when a production spec matters.

## Process
1. Identify the app's core purpose and brand language. Use previously established branding if relevant, otherwise choose a distinctive visual metaphor.
2. Reduce the metaphor to **one** recognizable core symbol with bold, filled, simple shapes and a clear silhouette. Avoid tiny details, busy texture, thin strokes, screenshots, unnecessary text, and excessive gloss.
3. Choose a deliberate, restrained palette and clear foreground/background contrast. Center the primary icon *optically* and leave a generous safe area for system masks.
4. Design to remain identifiable at small sizes. Preview at full size, 180 px, 60 px and 30 px (design tests, not Apple-prescribed pixel requirements).
5. Consider default, dark, clear and tinted modes. Preserve concept and recognizability across appearances.
6. Review the QA checklist; simplify any element that becomes noise at small scale.
7. Produce highest-quality assets in formats actually supported by the available tools. Never claim vector/editable source or variants if they haven't been made.

## Apple Human Interface Guidelines
- Prefer simplicity and immediate recognition. Fine features can become noisy once the system adds highlights and shadows.
- Prefer illustrations to photos and don't merely reproduce app UI.
- Avoid extremely thin lines and sharp angles if their detail is lost at smaller sizes.
- Avoid nonessential words, slogans or platform-specific statements.
- Do not replicate Apple hardware.
- Use unmasked square layers; the system applies corners/circular masks itself. Do **not** bake rounded corners into base artwork.
- Position important content centrally so system masking doesn't truncate it.
- Icons should maintain visual consistency across devices and appearances.

## Apple sizes and system shapes (verified 2026-10-24)
| Target | Canvas | System mask |
| --- | --- | --- |
| iOS, iPadOS, macOS | 1024 × 1024 px | rounded rectangle |
| watchOS | 1088 × 1088 px | circle |
| visionOS | 1024 × 1024 px | circle |
| tvOS | 800 × 480 px | rounded rectangle |

- Use sRGB for portable exports; Display P3 is also supported on Apple platforms as documented.
- For the contemporary Apple workflow, prefer layered artwork and Icon Composer to preview platforms and appearance variants (default, dark, clear light/dark, tinted light/dark).
- Draw artwork as vectors and export each independently adjustable layer as SVG when possible, converting text to outlines. PNG layers are suitable if SVG features are unsupported.
- **Defer** blur, shadows, specular effects, translucency, opacity, gradients and background effects to Icon Composer when preparing Liquid Glass layered icons.
- Background must cover the full canvas. For a static iOS icon, default to a fully opaque full-bleed backdrop. A transparent isolated glyph is a different asset type, not a complete icon.
- The system applies masks; do not export mask geometry on artwork layers.
- Flat 1024px PNG can be delivered for static icon workflows, but it is not equivalent to a layered Icon Composer `.icon` asset.

## QA checklist
- [ ] One memorable concept, recognisable silhouette
- [ ] Legible at small size and in grayscale
- [ ] Limited colours and strong contrast
- [ ] No unnecessary words, texture, fine details, or screenshots
- [ ] Optical centering and safe edge spacing
- [ ] Source artwork square and unmasked, background full-bleed
- [ ] Reviewed against dark, tinted and clear appearances
- [ ] Correct target platform size, color space, and export format
- [ ] Claims about editability, layers and formats match actual files

## User's current brain/maths app: optional brand-specific overlay
Use only for this specific project, not all apps:
- Three **solid** colours maximum; palette drawn from cobalt/electric blue, violet and magenta-pink (or deep navy when appropriate).
- **No gradients** unless user overrides.
- Abstract, simplified brain silhouette with a handful of bold lobes; no hyperdetailed anatomical illustration.
- Minimal, recognisable and attractive at small icon sizes. Depth should be restrained and should not add more colours.
- App icon background is part of the composition, not transparent (unless separate symbol layer requested).

## Image-generation brief template
'Create a square app icon for [APP], with one memorable central symbol [SYMBOL], composed of a small number of solid high-contrast shapes in [PALETTE], on a full-bleed opaque [BACKGROUND] backdrop. Center by visual weight, allow generous breathing space around outer edges, avoid gradients [if requested], letters, interface elements and minor detail, strong recognition at tiny sizes, no built-in rounded-corner mask.'

## Source of truth
1. Apple HIG app icons: https://developer.apple.com/design/human-interface-guidelines/app-icons
2. Apple's Icon Composer workflow: https://developer.apple.com/documentation/xcode/creating-your-app-icon-using-icon-composer
3. Apple Design Resources: https://developer.apple.com/design/resources/
4. Apple Icon Composer: https://developer.apple.com/icon-composer/

Design advice is a synthesis; check current Apple specifications before release. This is a portable skill document, not proof that it is registered as an executable system/plugin skill.
