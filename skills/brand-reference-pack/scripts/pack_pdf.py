# Renders a brand pack's README.md as a branded PDF (cover, palette + type plates, screenshot plates), laid out by an
# app's pdf.json (see apps/getahead/pdf.json for every field).
#   python3 .claude/skills/brand-reference-pack/scripts/pack_pdf.py apps/getahead/pdf.json
# Needs python `markdown` + PIL, and a playwright-core install (cfg "playwright"); system Chrome prints the PDF.
import json, re, subprocess, sys, tempfile, html
from pathlib import Path
import markdown
from PIL import Image

SKILL = Path(__file__).resolve().parents[1]
ROOT = SKILL.parents[2]
cfg = json.loads((SKILL / (sys.argv[1] if len(sys.argv) > 1 else 'apps/getahead/pdf.json')).read_text())
BRAND = ROOT / cfg['brand_dir']
def path(p): return ROOT / p[1:] if p.startswith('/') else BRAND / p
OUT = path(cfg['out'])
tok = json.loads((BRAND / 'tokens.json').read_text())
def token(ref):
    v = tok
    for k in ref.split('.'): v = v[k]
    return v
ACCENT, FAMILY = cfg.get('accent', '#ffffff'), cfg['font']['family']
tmp = Path(tempfile.mkdtemp(prefix='packpdf-'))

def strip(name, files, h=900, gap=24, crop=None):
    """Side-by-side plate of screenshots at a fixed height, saved as a compact JPEG."""
    ims = [Image.open(f).convert('RGB') for f in files]
    if crop: ims = [im.crop((0, int(im.height * crop[0]), im.width, int(im.height * crop[1]))) for im in ims]
    ims = [im.resize((round(im.width * h / im.height), h), Image.LANCZOS) for im in ims]
    plate = Image.new('RGB', (sum(i.width for i in ims) + gap * (len(ims) - 1), h), 'black')
    x = 0
    for im in ims: plate.paste(im, (x, 0)); x += im.width + gap
    p = tmp / f'{name}.jpg'; plate.save(p, quality=84); return p.as_uri()

PLATES = [(pl['title'], pl['caption'], strip(f'plate{i}', [path(f) for f in pl['files']], h=pl.get('h', 900), crop=pl.get('crop')))
          for i, pl in enumerate(cfg['plates'])]

def chip(name, hexv, sub=''):
    return f'<div class="sw"><i style="background:{hexv}"></i><b>{html.escape(name)}</b><span>{hexv}{(" · " + sub) if sub else ""}</span></div>'
pal = cfg.get('palette')
swatches = pal and ('<div class="plate">'
    + ''.join(f'<h4>{html.escape(g["title"])}</h4><div class="sws">' + ''.join(chip(c[0], token(c[1]), *c[2:]) for c in g['chips']) + '</div>'
              for g in pal['groups'])
    + (f'<h4>{html.escape(pal["bars"]["title"])}</h4>'
       + ''.join(f'<div class="bar"><span>{html.escape(n)}</span>' + ''.join(f'<i style="background:{c}"></i>' for c in token(r)) + '</div>'
                 for n, r in pal['bars']['rows']) if 'bars' in pal else '')
    + '</div>')
sp = cfg.get('specimen')
specimen = sp and (f'<div class="plate spec"><h4>Type — {html.escape(FAMILY)}</h4>'
    + ''.join(f'<p class="{c}">{html.escape(t)}</p>' for c, t in sp['lines'])
    + '<p>' + ' '.join(f'<span class="pill">{html.escape(t)}</span>' for t in sp.get('pills', []))
    + (f' <span class="pill sk"><i></i>{html.escape(sp["accentPill"])}</span>' if sp.get('accentPill') else '') + '</p></div>')

# Cover image: a square crop (x0, y0, x1 as fractions of the screenshot) of the hero visual.
cv = cfg['cover']; im = Image.open(path(cv['image'])).convert('RGB'); w, h = im.size; x0, y0, x1 = cv['crop']
im.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y0) + int(w * (x1 - x0)))).save(tmp / 'cover.jpg', quality=88)

md = (BRAND / 'README.md').read_text().replace('- [ ] ', '- ☐ ')
body = markdown.markdown(md, extensions=['tables', 'sane_lists'])
for block, conf in [(swatches, pal), (specimen, sp)]:
    if block: body = body.replace(f'<h3>{conf["before"]}</h3>', block + f'<h3>{conf["before"]}</h3>', 1)
body = re.sub(r'<h1>(.*?)</h1>', '', body, count=1)  # title goes on the cover
intro = '<h2>Visual references</h2><p>Screens from the captured surfaces. Full set in <code>refs/</code>.</p>'
plates = ''.join(f'<section class="pl">{intro if i == 0 else ""}<p class="eye">{i + 1:03d}/</p><h2>{html.escape(t)}</h2><img src="{src}"><p class="cap">{html.escape(c)}</p></section>'
                 for i, (t, c, src) in enumerate(PLATES))
faces = ''.join(f"@font-face{{font-family:'{FAMILY}';font-weight:{wt};src:url('{(path(cfg['font']['dir']) / f).as_uri()}')}}"
                for wt, f in cfg['font']['files'].items())
F = f"'{FAMILY}'"

doc = f'''<!doctype html><html><head><meta charset="utf-8"><style>
{faces}
@page {{ size: A4; margin: 0 }}
html {{ background:#000; -webkit-print-color-adjust:exact; print-color-adjust:exact }}
body {{ margin:0; background:#000; color:#fff; font:400 10.5pt/1.5 {F}; }}
main {{ padding:18mm 16mm; box-decoration-break:clone; -webkit-box-decoration-break:clone }}
.cover {{ height:297mm; box-sizing:border-box; padding:22mm 18mm; display:flex; flex-direction:column; break-after:page;
  background: radial-gradient(circle at 50% 56%, #fff3 0, #0000 22%), #000; }}
.cover img.wm {{ width:62mm }} .cover .hero {{ flex:1; display:flex; align-items:center; justify-content:center }}
.cover .hero img {{ width:110mm; border-radius:{'50%' if cv.get('round') else '8px'}; }}
.cover h1 {{ font:300 34pt/1.05 {F}; letter-spacing:-.03em; margin:0 0 6mm }} .cover p {{ color:#838383; margin:0 }}
h2 {{ font:300 24pt/1.1 {F}; letter-spacing:-.025em; margin:16mm 0 5mm; break-after:avoid }}
main > h2:first-of-type {{ margin-top:0 }}
h2 + * {{ break-before:avoid }}
h3 {{ font:500 13.5pt/1.2 {F}; letter-spacing:-.01em; margin:8mm 0 3mm; break-after:avoid }}
h4 {{ font:700 7.5pt {F}; letter-spacing:.2em; text-transform:uppercase; color:#ffffff80; margin:5mm 0 2.5mm }}
hr {{ border:0; margin:0 }}
p, li {{ color:#ffffffd9 }} strong {{ color:#fff; font-weight:500 }} em {{ color:#fff }}
a {{ color:{ACCENT}; text-decoration:none }}
code {{ font:9pt ui-monospace,Menlo,monospace; color:{ACCENT}; background:{ACCENT}14; padding:0 3px; border-radius:3px }}
blockquote {{ margin:5mm 0; padding:4mm 5mm; border-left:2px solid #fff; background:#161616; border-radius:0 8px 8px 0 }}
blockquote p {{ margin:0 }}
table {{ width:100%; border-collapse:collapse; margin:3mm 0 5mm; font-size:9pt; break-inside:auto }}
tr {{ break-inside:avoid }}
th {{ text-align:left; font:700 7pt {F}; letter-spacing:.16em; text-transform:uppercase; color:#ffffff80; border-bottom:1px solid #515151; padding:2mm 2.5mm }}
td {{ border-bottom:1px solid #1F1F1F; padding:2mm 2.5mm; vertical-align:top; color:#ffffffd9 }}
ul, ol {{ padding-left:5mm }} li {{ margin:1mm 0 }}
.plate {{ background:#0b0b0b; border:1px solid #1F1F1F; border-radius:10px; padding:4mm 5mm 5mm; margin:5mm 0; break-inside:avoid }}
.sws {{ display:grid; grid-template-columns:repeat(3,1fr); gap:3mm }}
.sw i {{ display:block; height:14mm; border-radius:6px; border:1px solid #ffffff1f; margin-bottom:1.5mm }}
.sw b {{ display:block; font-weight:500; font-size:9pt }} .sw span {{ font:8pt ui-monospace,Menlo,monospace; color:#838383 }}
.bar {{ display:flex; align-items:center; gap:2mm; margin:1.5mm 0 }} .bar span {{ width:34mm; font-size:8.5pt; color:#838383 }}
.bar i {{ flex:1; height:7mm; border-radius:4px }}
.spec .s-hook {{ font:400 26pt/1.02 {F}; letter-spacing:-.03em; margin:2mm 0 5mm; color:#fff }}
.spec .s-eye {{ font:700 7.5pt {F}; letter-spacing:.24em; color:#ffffff80; margin:0 0 1mm }}
.spec .s-head {{ font:400 16pt/1.1 {F}; letter-spacing:-.02em; color:#fff; margin:0 0 3mm }}
.spec .s-body {{ font:300 11pt/1.4 {F}; color:#ffffffb3 }}
.pill {{ display:inline-block; font:500 7.5pt {F}; letter-spacing:.12em; padding:1.5mm 3mm; border-radius:99px;
  background:#ffffff14; border:1px solid #ffffff66 }}
.pill.sk {{ letter-spacing:0; font-size:8.5pt; background:{ACCENT}24; border-color:{ACCENT}4d; color:{ACCENT} }}
.pill.sk i {{ display:inline-block; width:5px; height:5px; border-radius:50%; background:{ACCENT}; margin-right:4px; vertical-align:middle }}
.pl {{ break-before:page; }} .pl img {{ width:100%; border-radius:8px; display:block }}
.pl .eye {{ font:400 9pt {F}; color:#838383; margin:8mm 0 1mm }} .pl h2 {{ margin-top:0 }}
.pl > .eye:first-child {{ margin-top:0 }}
.pl .cap {{ color:#838383; font-size:9pt; margin-top:3mm }}
</style></head><body>
<div class="cover">
  <img class="wm" src="{path(cfg['wordmark']).as_uri()}">
  <div class="hero"><img src="{(tmp / 'cover.jpg').as_uri()}"></div>
  <h1>{cfg['title']}</h1>
  <p>{html.escape(cfg['subtitle'])}</p>
</div>
<main>{body}{plates}</main>
</body></html>'''

(tmp / 'pack.html').write_text(doc)
js = f'''const {{createRequire}}=require('module');const r=createRequire({json.dumps(str(path(cfg['playwright'])))});
const {{chromium}}=r('playwright-core');(async()=>{{const b=await chromium.launch({{channel:'chrome'}});const p=await b.newPage();
await p.goto({json.dumps((tmp / 'pack.html').as_uri())});await p.evaluate(()=>document.fonts.ready);
await p.pdf({{path:{json.dumps(str(OUT))},format:'A4',printBackground:true,preferCSSPageSize:true}});await b.close();}})();'''
subprocess.run(['node', '-e', js], check=True)
print(OUT, tmp / 'pack.html')
