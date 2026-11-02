#!/usr/bin/env python3
"""Check an App Store title, subtitle and keyword field before they ship.

Usage:
  check_metadata.py --title "Mental Math: 7 Minute" --subtitle "Brain Training for Adults" \
                    --keywords "times,tables,practice,drill"

FAIL (exit 1): over a character limit, or an Apple product name in the title or subtitle
(guideline 5.2.5 rejection). WARN: characters wasted, since Apple combines the words of all
three fields: a keyword-field word already in the title or subtitle, a word repeated in the
field, spaces after commas, or a plural whose singular is already there.
"""
import argparse, re, sys

LIMITS = {"title": 30, "subtitle": 30, "keywords": 100}
APPLE_NAMES = r"\b(iphone|ipad|apple watch|airpods|apple tv|macbook|imac|mac)\b"


def words(text):
    return re.findall(r"[\w']+", text.lower())


def check(title, subtitle, keywords):
    """Returns (fails, warns), each a list of messages."""
    fails, warns = [], []
    for field, text in (("title", title), ("subtitle", subtitle), ("keywords", keywords)):
        if len(text) > LIMITS[field]:
            fails.append(f"{field} is {len(text)}/{LIMITS[field]} characters")
    for field, text in (("title", title), ("subtitle", subtitle)):
        m = re.search(APPLE_NAMES, text.lower())
        if m:
            fails.append(f"{field} names an Apple product ({m.group(0)!r}); put it in the keyword field instead")
    if re.search(r"\s,|,\s", keywords):
        warns.append("spaces around commas in the keyword field waste characters")
    shown = set(words(title) + words(subtitle))
    seen = set()
    kw = words(keywords)
    for w in kw:
        if w in shown:
            warns.append(f"{w!r} is already in the title or subtitle")
        elif w in seen:
            warns.append(f"{w!r} appears twice in the keyword field")
        elif w.endswith("s") and w[:-1] in shown | set(kw):
            warns.append(f"{w!r} is a plural of {w[:-1]!r}, which is already covered")
        seen.add(w)
    return fails, warns


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--keywords", default="")
    a = ap.parse_args()
    fails, warns = check(a.title, a.subtitle, a.keywords)
    for field in ("title", "subtitle", "keywords"):
        print(f"  {field}: {len(getattr(a, field))}/{LIMITS[field]}")
    for m in fails:
        print(f"  FAIL  {m}")
    for m in warns:
        print(f"  WARN  {m}")
    print("ok" if not fails else f"{len(fails)} failure(s)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
