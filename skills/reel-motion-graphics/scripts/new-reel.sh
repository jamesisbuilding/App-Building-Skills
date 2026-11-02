#!/usr/bin/env bash
# Scaffold a new reel project from the kit template (a working copy of the Upcycling reel).
# Usage: new-reel.sh <target-dir> [presenter-image-or-video]
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
target="${1:?usage: new-reel.sh <target-dir> [presenter-file]}"
[ -e "$target" ] && { echo "refusing: $target already exists" >&2; exit 1; }
cp -R "$here/template" "$target"
name="$(basename "$target")"
sed -i '' "s/\"name\": \"reel\"/\"name\": \"$name\"/" "$target/package.json"
printf '{"id":"%s","name":"%s"}\n' "$name" "$name" > "$target/meta.json"
if [ -n "${2:-}" ]; then
  case "$(printf %s "$2" | tr "[:upper:]" "[:lower:]")" in
    *.mp4|*.mov|*.webm) cp "$2" "$target/assets/presenter.mp4"; echo "presenter video copied: swap the <img id=\"presenter\"> for a <video> (see SKILL.md)";;
    *) cp "$2" "$target/assets/presenter.jpg";;
  esac
fi
echo "scaffolded $target"
