#!/usr/bin/env bash
# List px values that are not multiples of 4 in a reel project's CSS/compositions.
# Expected leftovers: hairline borders (1–2px), glow/blur radii, and motion offsets in tweens.
# Usage: audit-grid.sh <reel-dir>
cd "${1:?usage: audit-grid.sh <reel-dir>}"
grep -noE '[^0-9.#a-zA-Z-](-?[0-9]+(\.[0-9]+)?)px' brand.css compositions/*.html index.html \
  | awk -F: '{v=$3; gsub(/[^0-9.-]/,"",v); if (v%4!=0) print $1":"$2": "v"px"}' | sort -u
