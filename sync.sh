#!/bin/zsh
# Copies my custom skills from ~/.claude/skills into this repo and pushes.
# New skill? Add its folder name to SKILLS and run ./sync.sh
set -e
cd "${0:A:h}"

SKILLS=(
  app-arbitrage
  app-keyword-research
  app-offer
  appicon-creator
  create-app
  app-set-up-infra
  new-app-info
  deep-work
)

# Private or copyrighted: never published.
EXCLUDES=(--exclude .DS_Store --exclude examples/ --exclude 100m-offers-transcript.txt --exclude __pycache__/)

for s in $SKILLS; do
  src=~/.claude/skills/$s
  [[ -f $src/SKILL.md ]] || { echo "missing: $src/SKILL.md" >&2; exit 1; }
  rsync -aL --delete $EXCLUDES "$src/" "skills/$s/"
  # Drop README rows pointing at the excluded files.
  [[ -f skills/$s/README.md ]] && sed -i '' -e '/examples\//d' -e '/100m-offers-transcript/d' skills/$s/README.md
done

# Remove published skills that are no longer in SKILLS.
for d in skills/*(/N); do
  (( ${SKILLS[(Ie)${d:t}]} )) || rm -rf "$d"
done

git add -A
git diff --cached --quiet && { echo "nothing to sync"; exit 0; }
git commit -m "sync skills $(date +%F)"
git push
