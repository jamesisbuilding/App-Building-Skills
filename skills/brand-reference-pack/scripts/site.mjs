// Captures a website for the reference pack: full-page + hero screenshots (desktop, mobile) and a JSON dump of the
// fonts, text colours, backgrounds, images and links actually used on the page.
//   node .claude/skills/brand-reference-pack/scripts/site.mjs https://www.getaheadmindset.com/ shader-lab/brand/refs/web
// Uses shader-lab's playwright-core and the system Chrome.
import { createRequire } from 'node:module';
import fs from 'node:fs';
const require = createRequire(new URL('../../../../shader-lab/package.json', import.meta.url));
const { chromium } = require('playwright-core');

const [url, out] = process.argv.slice(2);
if (!url || !out) { console.error('usage: node site.mjs <url> <out-dir>'); process.exit(2); }
fs.mkdirSync(out, { recursive: true });

const b = await chromium.launch({ channel: 'chrome' });
try {
  for (const [name, viewport, isMobile] of [['desktop', { width: 1440, height: 900 }, false], ['mobile', { width: 390, height: 844 }, true]]) {
    const p = await b.newPage({ viewport, deviceScaleFactor: 2, isMobile });
    await p.goto(url, { waitUntil: 'load', timeout: 60000 }); // not networkidle: Wix pages never go idle
    // Scroll through once so scroll-reveal sections render before the full-page shot.
    const h = await p.evaluate(() => document.body.scrollHeight);
    for (let y = 0; y < h; y += 400) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(250); }
    await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(1500);
    await p.screenshot({ path: `${out}/site-${name}-full.png`, fullPage: true });
    await p.screenshot({ path: `${out}/site-${name}-hero.png` });
    if (name !== 'desktop') continue;
    const styles = await p.evaluate(() => {
      const fonts = {}, colors = {}, bgs = {};
      for (const el of document.querySelectorAll('body *')) {
        const s = getComputedStyle(el);
        if (s.backgroundColor !== 'rgba(0, 0, 0, 0)') bgs[s.backgroundColor] = (bgs[s.backgroundColor] ?? 0) + 1;
        if (s.backgroundImage.includes('gradient')) bgs[s.backgroundImage] = (bgs[s.backgroundImage] ?? 0) + 1;
        if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
        const f = `${s.fontFamily.split(',')[0]} ${s.fontWeight} ${s.fontSize}/${s.lineHeight} ls=${s.letterSpacing} ${s.textTransform}`;
        (fonts[f] ??= []).length < 3 && fonts[f].push(el.innerText.trim().slice(0, 50));
        colors[s.color] = (colors[s.color] ?? 0) + 1;
      }
      return {
        fonts, colors, bgs,
        // Wix hides real font names behind wfont_* ids; the original name is in the inline style fallbacks (e.g. orig_satoshi_regular).
        fontNames: [...new Set([...document.querySelectorAll('[style*="font-family"]')].flatMap(e => e.style.fontFamily.match(/orig_[a-z_]+/g) ?? []))],
        imgs: [...new Set([...document.querySelectorAll('img')].map(i => i.currentSrc || i.src).filter(Boolean))],
        links: [...new Set([...document.querySelectorAll('a')].map(a => a.href).filter(h => h.startsWith('http')))],
        text: document.querySelector('main')?.innerText ?? document.body.innerText,
      };
    });
    fs.writeFileSync(`${out}/site-styles.json`, JSON.stringify(styles, null, 1));
  }
} finally { await b.close(); }
console.log(`wrote ${out}/site-{desktop,mobile}-{full,hero}.png and site-styles.json`);
