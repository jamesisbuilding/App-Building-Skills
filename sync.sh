#!/bin/zsh
# Copies my custom skills into this repo and pushes.
# New skill? Add "name|source folder|extra rsync excludes" to SKILLS and run ./sync.sh
set -e
cd "${0:A:h}"
S=~/.claude/skills
P=~/Desktop/"Side Projects"

SKILLS=(
  "app-arbitrage|$S/app-arbitrage|"
  "app-keyword-research|$S/app-keyword-research|"
  "app-offer|$S/app-offer|"
  "appicon-creator|$S/appicon-creator|"
  "create-app|$S/create-app|"
  "app-set-up-infra|$S/app-set-up-infra|"
  "new-app-info|$S/new-app-info|"
  "deep-work|$S/deep-work|"
  "brand-reference-pack|$P/GetAhead/.claude/skills/brand-reference-pack|apps/getahead/"
  "reel-script|$P/Reel Creator/.claude/skills/reel-script|"
  "reel-motion-graphics|$P/Reel Creator/.claude/skills/reel-motion-graphics|node_modules/ renders/"
  # The channel-brain skills need the driver scripts next to them, so publish the project minus its data.
  "channel-brain|$P/channel-brain|brains/ team/ .agents/ *.pdf personal-brand-vision.md RESUME.md shoot-day-1.md weekly-3-1-2-1-sheet.md zero-to-100-app-playbook.html"
)

# Private or copyrighted: never published.
BASE=(.DS_Store examples/ 100m-offers-transcript.txt __pycache__/)

names=()
for entry in $SKILLS; do
  IFS='|' read -r name src extra <<< "$entry"
  names+=$name
  [[ -f $src/SKILL.md || -d $src/.claude/skills ]] || { echo "no skill at: $src" >&2; exit 1; }
  ex=()
  for e in $BASE ${=extra}; do ex+=(--exclude "$e"); done
  rsync -aL --delete $ex "$src/" "skills/$name/"
  # Drop README rows pointing at the excluded files.
  [[ -f skills/$name/README.md ]] && sed -i '' -e '/examples\//d' -e '/100m-offers-transcript/d' skills/$name/README.md
done

# Remove published skills that are no longer listed.
for d in skills/*(/N); do
  (( ${names[(Ie)${d:t}]} )) || rm -rf "$d"
done

git add -A
git diff --cached --quiet && { echo "nothing to sync"; exit 0; }
git commit -m "sync skills $(date +%F)"
git push
