// Build preview.html: a single-file live player for the reel project, for the artifact.
// Inlines brand.css, every sub-composition host in index.html, and the presenter image,
// then drives all registered timelines from one master timeline with play / scrub controls.
// Usage: node build-preview.mjs → dist/preview.html (kept out of the project root so HyperFrames sees one entry point)
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';

const read = f => readFileSync(new URL(f, import.meta.url), 'utf8');
const index = read('index.html');
const attr = (tag, name) => (tag.match(new RegExp(`${name}="([^"]*)"`)) || [])[1];
const duration = Number(attr(index.match(/<div[^>]*id="root"[^>]*>/)[0], 'data-duration'));

// brand tokens; Google Fonts replaces the local @font-face files the render uses
const brand = read('brand.css').replace(/@font-face\{[^}]*\}\n?/g, '');
const fold = Number(brand.match(/--fold:(\d+)px/)[1]);

// each sub-composition: its <template> body, with its #root renamed so three roots can coexist
const hosts = [...index.matchAll(/<div[^>]*data-composition-src="[^"]*"[^>]*>/g)].map(([tag]) => {
  const id = attr(tag, 'data-composition-id');
  const tpl = read(attr(tag, 'data-composition-src')).match(/<template>([\s\S]*)<\/template>/)[1];
  const style = (tpl.match(/<style>([\s\S]*?)<\/style>/) || [, ''])[1].replaceAll('#root', `#${id}-root`);
  const script = (tpl.match(/<script>([\s\S]*?)<\/script>/) || [, ''])[1];
  const markup = tpl.replace(/<style>[\s\S]*?<\/style>|<script>[\s\S]*?<\/script>/g, '').trim()
    .replace(/id="root"/, `id="${id}-root"`);
  return { id, start: Number(attr(tag, 'data-start')), dur: Number(attr(tag, 'data-duration')), style, script, markup };
});

const img = index.match(/<img[^>]*id="presenter"[^>]*>/)[0];
const imgSrc = attr(img, 'src');
const presenter = `data:image/jpeg;base64,${readFileSync(new URL(imgSrc, import.meta.url)).toString('base64')}`;

mkdirSync(new URL('dist/', import.meta.url), { recursive: true });
writeFileSync(new URL('dist/preview.html', import.meta.url), `<title>Upcycling in 30 Seconds</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,18,500;0,18,600;1,18,500&family=Instrument+Sans:wght@500;600&display=swap">
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<style>
/* Page chrome follows the viewer's theme; the 1080×1920 frame is a fixed dark world scaled to fit. */
:root{--page:#EADFCB;--ui-fg:#1A1109;--ui-muted:#5A4631;--ui-line:#CDB98F;--ui-accent:#8A6A3B;--ui-surface:#F5EEDF}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--page:#000;--ui-fg:#F1E4C8;--ui-muted:#A89573;--ui-line:#2E2216;--ui-accent:#DDBB7F;--ui-surface:#1A120A;color-scheme:dark}}
:root[data-theme="dark"]{--page:#000;--ui-fg:#F1E4C8;--ui-muted:#A89573;--ui-line:#2E2216;--ui-accent:#DDBB7F;--ui-surface:#1A120A;color-scheme:dark}
${brand}
*{box-sizing:border-box}
body{background:var(--page);color:var(--ui-fg);font:14px/1.5 var(--body);padding-inline:16px;padding-block:20px 32px}
.page{max-width:620px;margin-inline:auto;display:flex;flex-direction:column;gap:14px}
.meta{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font:500 12px var(--body);letter-spacing:.1em;text-transform:uppercase;color:var(--ui-muted)}
.ctl{display:flex;flex-wrap:wrap;gap:12px;align-items:center;position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--page);padding-block:8px}
.ctl button{font:500 13px var(--body);letter-spacing:.06em;text-transform:uppercase;color:var(--ui-fg);background:var(--ui-surface);border:1px solid var(--ui-fg);padding:8px 14px;border-radius:10px;cursor:pointer;min-width:84px}
.ctl button:hover{background:var(--ui-fg);color:var(--page)}
.ctl button:focus-visible,.ctl input:focus-visible{outline:2px solid var(--ui-accent);outline-offset:2px}
.ctl input[type=range]{flex:1 1 140px;min-width:0;accent-color:var(--ui-accent);margin:0}
.ctl output{font:400 12px var(--body);color:var(--ui-muted);font-variant-numeric:tabular-nums;white-space:nowrap}
.viewport{position:relative;width:100%;max-width:min(100%,calc(min(80vh,960px)*9/16));margin-inline:auto;aspect-ratio:9/16;border-radius:20px;overflow:hidden;box-shadow:0 0 0 1px var(--ui-line);background:#000}
.frame{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:0 0;overflow:hidden;background:var(--ink);color:var(--fg)}
.layer{position:absolute;inset:0}
#presenter{position:absolute;left:0;top:var(--fold);width:1080px;height:calc(1920px - var(--fold));object-fit:cover;object-position:center 20%}
.guides{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:10}
.guides[hidden]{display:none}
${hosts.map(h => h.style).join('\n')}
</style>

<main class="page">
  <div class="meta"><span>Sparse upcycling · HyperFrames kit</span><span>1080 × 1920 · ${duration} s · loops</span></div>
  <div class="ctl">
    <button id="pp" type="button">Pause</button>
    <input id="scrub" type="range" min="0" max="${duration * 100}" value="0" aria-label="Timeline">
    <output id="tm">0:00 / 0:${String(duration).padStart(2, '0')}</output>
    <button id="gbtn" type="button" aria-pressed="false">Guides</button>
  </div>
  <div class="viewport" id="viewport">
    <div class="frame" id="frame" role="img" aria-label="Animated explainer of sparse upcycling: a trained dense MLP is copied into eight glass experts, a router sends each token to two of them, training makes them diverge, and the result is 3.25 times the parameters for 1.32 times the compute per token">
${hosts.map(h => `      <div class="layer" id="host-${h.id}">\n${h.markup}\n      </div>`).join('\n')}
      <img id="presenter" src="${presenter}" alt="Presenter placeholder">
      <svg class="guides" id="guides" viewBox="0 0 1080 1920" hidden aria-hidden="true">
        <g fill="#ff4040" fill-opacity=".22"><rect x="0" y="0" width="1080" height="175"/><rect x="896" y="175" width="184" height="1505"/><rect x="0" y="1680" width="1080" height="240"/></g>
        <rect x="172" y="192" width="656" height="588" fill="none" stroke="#DDBB7F" stroke-width="3" stroke-dasharray="12 8"/>
        <rect x="172" y="812" width="656" height="92" fill="#DDBB7F" fill-opacity=".1" stroke="#DDBB7F" stroke-width="3" stroke-dasharray="12 8"/>
        <rect x="0" y="${fold}" width="1080" height="${1920 - fold}" fill="none" stroke="#fff" stroke-width="4" stroke-dasharray="16 8"/>
        <g font-family="Instrument Sans,Arial,sans-serif" font-weight="600" fill="#fff" fill-opacity=".9" letter-spacing="3">
          <text x="120" y="152" font-size="24">APP TOP BAR</text>
          <text x="988" y="340" font-size="20" text-anchor="middle">LIKES</text>
          <text x="500" y="760" font-size="24" text-anchor="middle">ANIMATION</text>
          <text x="500" y="925" font-size="24" text-anchor="middle">CAPTIONS</text>
          <text x="500" y="1400" font-size="28" text-anchor="middle">TALKING HEAD · ${1920 - fold} PX</text>
          <text x="120" y="1750" font-size="24">DESCRIPTION · SOUND · NAV BAR</text>
        </g>
      </svg>
    </div>
  </div>
</main>

<script>
window.__timelines = {};
${hosts.map(h => `(function(){\n${h.script}\n})();`).join('\n')}
(function(){
  const DUR=${duration}, HOSTS=${JSON.stringify(hosts.map(({ id, start, dur }) => ({ id, start, dur })))};
  const master=gsap.timeline({paused:true});
  HOSTS.forEach(h=>{const tl=window.__timelines[h.id];if(tl){tl.paused(false);master.add(tl,h.start)}});
  const frame=document.getElementById('frame'),vp=document.getElementById('viewport');
  const fit=()=>{frame.style.transform='scale('+(vp.clientWidth/1080)+')'};
  new ResizeObserver(fit).observe(vp);fit();
  const pp=document.getElementById('pp'),scrub=document.getElementById('scrub'),tm=document.getElementById('tm');
  const reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let t=reduce?DUR*.75:0,playing=!reduce,last=null,drag=false,dirty=true;
  const fmt=s=>Math.floor(s/60)+':'+String(Math.floor(s%60)).padStart(2,'0');
  function render(){
    master.seek(t,false);
    HOSTS.forEach(h=>{document.getElementById('host-'+h.id).style.visibility=(t>=h.start&&t<h.start+h.dur)?'visible':'hidden'});
    if(!drag)scrub.value=Math.round(t*100);
    tm.textContent=fmt(t)+' / '+fmt(DUR);pp.textContent=playing?'Pause':'Play';
  }
  function frameLoop(ts){
    if(last===null)last=ts;
    const dt=Math.min(.1,(ts-last)/1000);last=ts;
    if(playing&&!drag){t+=dt;if(t>=DUR)t-=DUR;dirty=true}
    if(dirty){render();dirty=false}
    requestAnimationFrame(frameLoop);
  }
  pp.addEventListener('click',()=>{playing=!playing;dirty=true});
  scrub.addEventListener('pointerdown',()=>{drag=true});
  ['pointerup','pointercancel','blur'].forEach(ev=>scrub.addEventListener(ev,()=>{drag=false}));
  scrub.addEventListener('input',()=>{t=+scrub.value/100;dirty=true});
  const guides=document.getElementById('guides'),gBtn=document.getElementById('gbtn');
  gBtn.addEventListener('click',()=>{guides.hidden=!guides.hidden;gBtn.setAttribute('aria-pressed',String(!guides.hidden))});
  if(document.fonts)document.fonts.ready.then(()=>{dirty=true});
  requestAnimationFrame(frameLoop);
})();
</script>
`);
console.log(`preview.html built: ${hosts.map(h => h.id).join(', ')} · ${duration}s`);
