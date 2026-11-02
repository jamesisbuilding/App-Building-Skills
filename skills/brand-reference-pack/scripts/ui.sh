#!/bin/bash
# ui.sh shot <name> | tree | tap x y | label "<text>" | swipe x1 y1 x2 y2 | hold x y secs
# Thin wrapper over .claude/uidriver: numbered screenshots go to $OUT (NN-name.png, in capture order).
# Env: UDID (booted sim, see `xcrun simctl list devices booted`), OUT (screenshot folder).
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
export UDID=${UDID:?set UDID to the booted simulator}
D=${OUT:?set OUT to the screenshot folder, e.g. <brand-dir>/refs/app}; mkdir -p "$D"
U="$ROOT/.claude/uidriver/uidriver.py"
case $1 in
  shot) n=$(ls "$D" | grep -c '^[0-9][0-9]-'); f=$(printf "%s/%02d-%s.png" "$D" $n "$2"); xcrun simctl io $UDID screenshot "$f" >/dev/null 2>&1; echo "$f";;
  tree) python3 "$U" tree;;
  tap) python3 "$U" tap $2 $3;;
  label) python3 "$U" taplabel "$2";;
  swipe) python3 "$U" swipe $2 $3 $4 $5;;
  hold) idb ui tap $2 $3 --duration $4 --udid $UDID;;
esac
