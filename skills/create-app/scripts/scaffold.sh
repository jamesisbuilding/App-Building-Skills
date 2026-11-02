#!/usr/bin/env bash
# Usage: scaffold.sh <snake_name> "<Display Title>" [parent_dir] [apple_team_id]
# Creates <parent_dir>/<snake_name>: flutter create + the layered Cubit template,
# latest compatible packages, then analyze + every test suite as a self-check.
set -euo pipefail

name=$1; title=$2; parent=${3:-$PWD}; team=${4:-}
tpl="$(cd "$(dirname "$0")/../template" && pwd)"
dir="$parent/$name"

[[ $name =~ ^[a-z][a-z0-9_]*$ ]] || { echo "name must be snake_case: $name" >&2; exit 1; }
[[ -e $dir ]] && { echo "already exists: $dir" >&2; exit 1; }

export NAME=$name TITLE=$title
export DART=$(dart --version 2>&1 | sed -E 's/.*version: ([0-9]+\.[0-9]+).*/\1/').0

flutter create --org com --platforms ios,android --empty --project-name "$name" "$dir"
rm -rf "$dir/lib" "$dir/test" "$dir/pubspec.yaml" "$dir/analysis_options.yaml"
cp -R "$tpl"/. "$dir"/
cd "$dir"
grep -rlE '__app__|__title__|__dart__' lib test packages pubspec.yaml CLAUDE.md \
  | xargs perl -pi -e 's/__app__/$ENV{NAME}/g; s/__title__/$ENV{TITLE}/g; s/__dart__/$ENV{DART}/g'

# Home-screen name
export XML_TITLE=$(TITLE=$title perl -e '$_=$ENV{TITLE}; s/&/&amp;/g; s/</&lt;/g; s/>/&gt;/g; s/"/&quot;/g; print')
perl -0pi -e 's|(<key>CFBundleDisplayName</key>\s*<string>)[^<]*|$1$ENV{XML_TITLE}|' ios/Runner/Info.plist
perl -pi -e 's|<application|<application android:allowBackup="false"|' android/app/src/main/AndroidManifest.xml  # adb backup could copy app data
perl -pi -e 's|android:label="[^"]*"|android:label="$ENV{XML_TITLE}"|' android/app/src/main/AndroidManifest.xml

if [[ -n $team ]]; then  # flutter create picks Xcode's first team; replace it, Runner target only
  perl -ni -e 'print unless /DEVELOPMENT_TEAM = /' ios/Runner.xcodeproj/project.pbxproj
  perl -pi -e "s/^(\s*)(PRODUCT_BUNDLE_IDENTIFIER = [^;]*;)/\$1\$2\n\$1DEVELOPMENT_TEAM = $team;/ unless /RunnerTests/" \
    ios/Runner.xcodeproj/project.pbxproj
fi

(cd packages/storage_client && flutter pub add shared_preferences && flutter pub add --dev mocktail very_good_analysis)
(cd packages/settings_repository && flutter pub add --dev mocktail very_good_analysis)
flutter pub add bloc flutter_bloc intl
flutter pub add --dev bloc_test mocktail very_good_analysis bloc_lint

dart fix --apply
dart format .
flutter analyze
flutter test
for p in packages/*/; do (cd "$p" && flutter test); done
echo "OK: $dir"
