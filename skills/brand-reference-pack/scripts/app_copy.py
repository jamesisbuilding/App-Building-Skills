#!/usr/bin/env python3
"""Pull an app's user-facing copy out of its source: every string literal of 3+ words that reads as prose, with file:line.

    python3 app_copy.py <src root> <out.md> [ui dir or file …]
    e.g. python3 app_copy.py app/lib persona/raw/app-copy/app-copy-<date>.md app/lib/pages app/lib/widgets app/lib/main.dart

Log lines, keys, ids, paths and API keys are filtered out; interpolations are left as written. Built for Dart/Flutter;
the literal regex also works for JS/TS/Swift/Kotlin sources (pass --ext). Read-only on the source tree.
"""
import collections, os, re, sys

args = [a for a in sys.argv[1:] if not a.startswith('--')]
ext = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--ext=')), '.dart')
if len(args) < 2: sys.exit(__doc__)
root, out, ui = args[0], args[1], tuple(args[2:]) or (args[0],)
LIT = re.compile(r"""(?<![\w$])(['"])((?:\\.|(?!\1).){12,}?)\1""")
BAD = re.compile(r"https?://|\.(dart|png|jpe?g|json|svg|gif|mp3|wav)\b|assets/|AIza|firebase|\bcom\.[a-z]|drawable/|^\s*\[|=>|::"
                 r"|\b(null|true|false)\b|Exception|Error:|_[a-z]+_|^[a-z]+(_[a-z]+)+$", re.I)
LOG = re.compile(r"\b(debugPrint|print|log|logger|Logger|developer\.log|console\.\w+|throw|assert|Sentry|crashlytics|analytics)\b", re.I)

def prose(s):
    return not BAD.search(s) and s.count(' ') >= 2 and sum(c.isalpha() or c == ' ' for c in s) >= .8 * len(s)

assert prose("Set a focus to tell us what you're training for") and not prose("AIzaSyD-abc def ghi") and not prose("[Splash] Auth loaded ok")

by, n = collections.OrderedDict(), 0
for dp, _, fs in sorted(os.walk(root)):
    for f in sorted(fs):
        p = os.path.join(dp, f)
        if not f.endswith(ext) or f.endswith(('.g.dart', '.freezed.dart')) or not p.startswith(ui): continue
        for i, line in enumerate(open(p, encoding='utf-8', errors='ignore'), 1):
            if LOG.search(line) or line.strip().startswith(('//', '///', 'import', 'export', 'part ')): continue
            for m in LIT.finditer(line):
                s = m.group(2).replace("\\'", "'")
                if prose(s): by.setdefault(p, []).append((i, s)); n += 1
os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
with open(out, 'w') as o:
    o.write(f"# In-app copy (verbatim string literals from the app's UI code)\n\nFrom `{', '.join(ui)}` (read-only). 3+ word prose "
            "literals with file:line; logs, keys, ids and paths filtered. Some may be dev-only or unused. CMS-served copy is not here.\n\n")
    for p, items in by.items():
        o.write(f"## {p}\n\n" + ''.join(f"- L{i}: {s}\n" for i, s in items) + "\n")
print(f"{n} strings in {len(by)} files → {out}")
