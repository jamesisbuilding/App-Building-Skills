## Branches

| Branch | What it is |
|---|---|
| `main` | Production: the version on the App Store. Every push builds and uploads to TestFlight. |
| `release/x.y.z` | One per version: where a release is tested, then kept as its history. |
| `develop` | The next release: finished work collects here. |
| `feat/…`, `fix/…`, `task/…` | One piece of work, branched from `develop`, e.g. `feat/ABC-12-streak-shield`. |

## Flow

1. **Work:** branch `feat/…`, `fix/…` or `task/…` from `develop`. When it's done and tested, merge it into `develop`.
2. **Release:** when `develop` is ready, branch `release/x.y.z` from it. Bump `version:` in `pubspec.yaml` to `x.y.z` (it must be higher than the live version), and test on a device (`tool/phone.sh`). Fixes go straight onto the release branch. Write the App Store "What's New" text in `release-notes/x.y.z.md` (one `## <locale>` section per store locale, plain text, under 4,000 characters) and commit it on the release branch.
3. **Promote:** merge `release/x.y.z` into `main` and push. CI builds it and uploads it to TestFlight (see below). Watch the run (`gh run watch`) until it's green. If it fails, fix it on the release branch and promote again. Then, in App Store Connect, add the build to version x.y.z, paste `release-notes/x.y.z.md` into What's New in This Version, and submit it for review.
4. **Back-merge:** merge `main` into `develop`, so any fixes made on the release branch aren't lost. Keep `release/x.y.z` as the record of that version.

**Hotfix:** branch `release/x.y.(z+1)` from `main`, fix, test, promote, back-merge.

## CI: TestFlight on every push to `main`

`.github/workflows/testflight.yml` runs the tests, then `tool/testflight.sh`, on a macOS runner. The build number is the time (e.g. `2611011430`). Signing is automatic through the App Store Connect API key, so there's no certificates repo. The key needs the **Admin** role (or access to cloud-managed distribution certificates), so Xcode can sign on a fresh machine. The obfuscation symbols are saved as a run artifact for 90 days, for decoding crash reports.

It can also be run by hand: Actions → TestFlight → Run workflow.

### Repository secrets

Settings → Secrets and variables → Actions:

| Secret | Value |
|---|---|
| `KEYS_JSON` | The whole of `keys.json`: the build keys, with live store keys only and no fake-purchase flags |
| `ASC_KEY_ID` | The App Store Connect API key ID (`ASC_KEY_ID` in `tool/asc.env`) |
| `ASC_ISSUER_ID` | The issuer ID (`ASC_ISSUER_ID` in `tool/asc.env`) |
| `ASC_KEY_P8` | The `AuthKey_<id>.p8` file, base64-encoded |

From this folder, with the GitHub CLI:

```bash
gh secret set KEYS_JSON < keys.json
```

```bash
source tool/asc.env && gh secret set ASC_KEY_ID --body "$ASC_KEY_ID" && gh secret set ASC_ISSUER_ID --body "$ASC_ISSUER_ID" && base64 -i "$ASC_KEY_PATH" | gh secret set ASC_KEY_P8
```

