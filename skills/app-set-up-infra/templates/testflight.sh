#!/bin/zsh
# Archive with the keys from keys.json and upload to TestFlight, signed through an App Store Connect API key,
# so no Apple ID needs to be signed in to Xcode. tool/asc.env (git-ignored) sets ASC_KEY_ID, ASC_ISSUER_ID and
# ASC_KEY_PATH (the AuthKey_XXXX.p8 file). The key file is only ever passed by path.
set -e
setopt pipefail # a failed export or upload fails the script (CI relies on it)
cd "$(dirname "$0")/.."
export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
source tool/asc.env
[[ -f "$ASC_KEY_PATH" ]] || { echo "No key file at $ASC_KEY_PATH" >&2; exit 1; }
grep -q DUMMY_PURCHASES keys.json && { echo 'keys.json must not set DUMMY_PURCHASES for a store build' >&2; exit 1; }
grep -q '"REVENUECAT_IOS_KEY": "test_' keys.json && { echo 'REVENUECAT_IOS_KEY is a Test Store key; put the appl_ key in keys.json' >&2; exit 1; }
auth=(-allowProvisioningUpdates -authenticationKeyPath "$ASC_KEY_PATH" -authenticationKeyID "$ASC_KEY_ID" -authenticationKeyIssuerID "$ASC_ISSUER_ID")
# Each upload needs a new build number: the time, e.g. 2610271430
flutter build ios --release --config-only --build-number=$(date +%y%m%d%H%M) \
  --dart-define-from-file=keys.json --obfuscate --split-debug-info=build/symbols
rm -rf build/ios/archive/Runner.xcarchive # so a failed archive can't upload the previous one
xcodebuild -workspace ios/Runner.xcworkspace -scheme Runner -configuration Release -destination generic/platform=iOS \
  -archivePath build/ios/archive/Runner.xcarchive archive "${auth[@]}" | grep -E "error|ARCHIVE" || true
[[ -d build/ios/archive/Runner.xcarchive ]] || exit 1
xcodebuild -exportArchive -archivePath build/ios/archive/Runner.xcarchive -exportPath build/ios/upload \
  -exportOptionsPlist tool/ExportUpload.plist "${auth[@]}" | grep -E "error|EXPORT|Upload"
