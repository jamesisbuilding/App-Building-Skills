---
name: app-set-up-infra
description: Sets up an iOS app's infrastructure. It creates the branches (main = prod, release/x.y.z per version, develop, and feat/fix/task branches), a private GitHub repo, and GitHub Actions CI that uploads every push to main to TestFlight, signed through an App Store Connect API key (no fastlane match, no certificates repo). It collects what only the user has (GitHub repo, API key ID, issuer ID, key file, team ID) with AskUserQuestion. It saves the answers in the project's git-ignored tool/asc.env for next time, and the user runs the secret-setting commands themselves. After every push it watches the CI run, checking once a minute, until it's green; on a failure it reads the log, fixes the cause on the right branch, pushes and watches again (up to 3 tries). Use it when the user says "/app-set-up-infra", "set up CI", "set up the branches and GitHub", "deploy to TestFlight on merge", "promote the release and watch CI", or "set up infra like 7 Minute Math". Built for Flutter iOS apps; see Scope for others.
---

# app-set-up-infra

Set up the branching convention, GitHub and TestFlight CI for an app. The user supplies keys and links (human in the loop); you do everything else. Read `RETRO.md` once: each rule below comes from something that went wrong there.

## The convention

| Branch | Role |
|---|---|
| `main` | Production: what's on the App Store. Every push builds and uploads to TestFlight. |
| `release/x.y.z` | One per version: tested here, promoted to `main`, then kept as that version's history. |
| `develop` | The next release. Finished work is merged here. |
| `feat/…`, `fix/…`, `task/…` | One piece of work from `develop`, optionally with a ticket code: `feat/ABC-12-short-name`. |

Flow:
1. Work on a branch from `develop`.
2. Merge it into `develop`.
3. Cut `release/x.y.z` and bump the version.
4. Test on a device.
5. Write the release notes (Step 6b) on the release branch.
6. Merge into `main`; CI uploads to TestFlight.
7. Submit in App Store Connect, pasting the release notes into What's New.
8. Merge `main` back into `develop`.

Hotfix: cut `release/x.y.(z+1)` from `main`.

After every push that starts a workflow run (`main`, or a branch with CI on it), watch the run until it's green (Step 6).

## Hard rules

1. **Never handle secret values.** Don't print, read into a script or type the `.p8` contents, `keys.json` values or tokens. Pass key files by path only. The user runs every `gh secret set` command; you check by listing names (`gh secret list`). Key IDs, issuer IDs, team IDs, bundle IDs and repo URLs are identifiers, not secrets, so those you can store and use.
2. **Never disturb the working copy.** It may be shared with other live sessions. Don't check out, reset, stash or `git add -A` there. Do branch work in a worktree (`git worktree add <scratch>/<name> <branch>`). Before committing uncommitted work, check its edit times (`stat`) to make sure nobody is mid-edit, run the analyzer and tests, and stage files by name.
3. **Pin anything tied to a release to its commit.** "The shipped version" is the commit that produced the build in App Store Connect, not the working copy.
4. **Don't put CI on `main` while that version is in review.** A push to `main` uploads a build. CI goes into `develop` and reaches `main` with the next release.
5. **No dependency on another org's repo or template.** Write a standalone workflow in the app's own repo.
6. **Check before you create.** Look at `git remote -v`, `git branch -a` and `gh repo view` before adding a remote, creating a repo or pushing. Another session or the user may already have done it.
7. **Pushing and creating repos are outward-facing.** Confirm with AskUserQuestion first, unless the user already said to.
8. **A push isn't done until its CI run is green.** Watch every run you start (Step 6). If it fails, fix the cause and push again. Never make it pass by skipping or weakening a test, removing a check from `testflight.sh`, or adding `continue-on-error`.

## Step 1: Read the project

- **The git state.** Branches, uncommitted files (`git status --porcelain`), remotes, and whether `main` exists. Work out what's shipped: the App Store version and build (ask in Step 2 if it isn't clear) and the commit that produced them.
- **The app.** Bundle ID and team (`PRODUCT_BUNDLE_IDENTIFIER`, `DEVELOPMENT_TEAM` in `ios/Runner.xcodeproj/project.pbxproj`); version (`pubspec.yaml`); Flutter and Xcode versions (`flutter --version`, `xcodebuild -version`).
- **Existing scripts.** Device and upload scripts (`tool/*.sh`, Makefile, fastlane). Reuse an existing API-key upload script rather than adding fastlane. Note any fake-purchase flags (`DUMMY_PURCHASES`, `MOCK`, a RevenueCat `test_` key) in device scripts.
- **Saved answers.** `tool/asc.env`, if it exists, holds them from a previous run. Use it and only ask for what's missing.
- **Key files.** Look in `keys/`, `tool/` and the project root for `AuthKey_<KEYID>.p8` (the App Store Connect API key; the key ID is in the filename) and `SubscriptionKey_<ID>.p8` (the In-App Purchase key, which CI doesn't need). List the file names only.
- **Build keys.** `keys.json` or `.env` for `--dart-define-from-file`. Check that it's git-ignored, and that no key file was ever committed: `git log --all --oneline -- keys.json '*.p8' '*.env'`.

## Step 2: Ask the user (AskUserQuestion)

Ask only for what Step 1 couldn't settle. Use up to 4 questions per call. Make the detected value the first option, marked "(Recommended)"; the user can always pick "Other" to type their own. Ask for these:

| Question | Header | Options to offer |
|---|---|---|
| Which GitHub repo should this use? | GitHub repo | "Create private `<gh user>/<app-slug>`" (from `gh auth status` and the app name) · "I've made one; I'll paste the URL" |
| What's your App Store Connect API key ID? | API key ID | The ID from an `AuthKey_<ID>.p8` filename · "I'll paste it" |
| What's the issuer ID? (App Store Connect → Users and Access → Integrations → App Store Connect API, at the top) | Issuer ID | "I'll paste it". It isn't in the `.p8` file, so never guess it |
| Where is the key file? | Key file | Each `.p8` found · "I'll paste the path" |
| Does that key have the Admin role? (Needed so CI can sign on a fresh machine.) | Key role | "Yes, Admin" · "No, I'll make an Admin key" |
| Which version is live or in review, and which commit is it? | Shipped | The `main` tip or the latest "shipped" commit, with its version · "Nothing shipped yet" |
| Merge the existing feature branches into `develop`? | Develop | "Merge all (Recommended)" · "Pick which" · "Start develop empty" (only when there are branches to merge) |

If an answer comes back as "I'll paste it" without the value, ask again, plainly, in chat.

**Save the answers** in `tool/asc.env` (create it from `templates/asc.env` if it doesn't exist). Make sure `.gitignore` covers `tool/asc.env`, `*.p8` and the build-keys file; if it doesn't, add them in the infra commit. The saved fields are `ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_KEY_PATH`, `GITHUB_REPO`, `APPLE_TEAM_ID`, `BUNDLE_ID` and `SHIPPED_VERSION`, `SHIPPED_COMMIT`. A later run reads them and skips those questions.

## Step 3: The branches

In worktrees, never in the working copy:

1. `release/<shipped version>` at the shipped commit. If `main` isn't there, point `main` at it too (if `main` has unshipped work, ask before moving it).
2. `develop` from `main`. Merge each feature branch with `--no-ff`:
   - **Check before merging old or `wip` branches.** If a later branch redid the same work, compare a few key identifiers on both sides (`git grep -c <id> <branch> -- lib`). If they're all already in `develop`, record the branch as merged without its changes (`git merge -s ours`) and say so in the message.
   - **Conflicts:** read both sides. Where both added something different, keep both; anything else, ask the user. Never leave conflict markers.
   - **After every merge:** run the analyzer and tests (`flutter analyze`, `flutter test`). Fix anything the merge broke in a separate commit.
3. Ask whether to commit the uncommitted work in the working copy to its branch (Hard rule 2). Then merge it.

## Step 4: CI

On a branch `task/ci-testflight` from `develop`:

1. **Upload script.** Keep the project's own script if it signs with the API key (`-allowProvisioningUpdates -authenticationKeyPath/-ID/-IssuerID`). Otherwise add `templates/testflight.sh` as `tool/testflight.sh` and `templates/ExportUpload.plist` as `tool/ExportUpload.plist`, with the team ID filled in. Either way, the script must:
   - set `pipefail` (so a failed export or upload fails the run);
   - refuse fake-purchase flags and test store keys;
   - use a new build number for each upload (the time);
   - delete any old archive before archiving.
2. **Workflow.** Add `templates/testflight.yml` as `.github/workflows/testflight.yml`, with the Flutter version filled in. Validate it (`python3 -c "import yaml; yaml.safe_load(open(...))"`), and check the script with `zsh -n`.
3. **README.** Add the branches, flow, CI and secrets sections from `templates/README-infra.md`.
4. Commit, then merge `task/ci-testflight` into `develop` (Hard rule 4).

## Step 5: GitHub

1. Check what's already there (Hard rule 6). Create the repo only on the user's yes: `gh repo create <owner>/<name> --private`.
2. Add `origin` if it's missing, then push `main`, `release/*`, `develop` and `task/ci-testflight`. Check the local and remote commits match, and that the repo is private with `main` as the default branch.
3. Give the user the secrets commands, with `--repo` filled in. They run them from the app folder:
   ```bash
   gh secret set KEYS_JSON --repo <owner>/<name> < keys.json
   ```
   ```bash
   source tool/asc.env && gh secret set ASC_KEY_ID --repo <owner>/<name> --body "$ASC_KEY_ID" && gh secret set ASC_ISSUER_ID --repo <owner>/<name> --body "$ASC_ISSUER_ID" && base64 -i "$ASC_KEY_PATH" | gh secret set ASC_KEY_P8 --repo <owner>/<name>
   ```
4. Once they say it's done, run `gh secret list --repo <owner>/<name>` and check all 4 names are there.

## Step 6: Watch CI after every push

Applies to every push that starts a run: during setup, and whenever the skill is used later to promote a release (`release/x.y.z` → `main`).

1. **Find the run for this commit:** `gh run list --repo <owner>/<name> --workflow testflight.yml --branch <branch> --limit 5 --json databaseId,headSha,status`. Take the run whose `headSha` is the commit you pushed. If it hasn't appeared, check again once a minute, for up to 3 minutes. If none appears, check the workflow is on that branch and its `on:` trigger matches.
2. **Wait for it,** checking once a minute: run `gh run watch <id> --repo <owner>/<name> --exit-status --interval 60` in the background (it exits when the run finishes) and carry on when it reports. Tell the user the run's URL (`gh run view <id> --json url`).
3. **Green:** report the run URL and the build number it uploaded (`gh run view <id> --log | grep -m1 'Upload'`, or the time-based number). Note that App Store Connect still processes the build for a few minutes before TestFlight shows it.
4. **Red:** read only the failing steps (`gh run view <id> --repo <owner>/<name> --log-failed | tail -80`) and find the cause:

   | Failure | Usual cause | Fix |
   |---|---|---|
   | Flutter setup | The version isn't on the stable channel | Pin the nearest stable release to the local one, in the workflow |
   | Xcode or SDK | The runner image doesn't have it | Choose a version the image has, in `setup-xcode` |
   | Test | A real failing test | Fix the code or the test's broken setup, never by skipping the test |
   | Write keys / missing secret | A secret is missing or misnamed | Ask the user to set it (`gh secret list` shows the names); never set it yourself |
   | Signing, `-allowProvisioningUpdates` | The key isn't Admin, or the team is wrong | Ask the user for an Admin key, or fix `ExportUpload.plist` |
   | Upload: version or build already used | The version wasn't bumped, or the build number repeats | Bump `version:` on the release branch |

5. **Fix on the right branch** (in a worktree, as always):
   - a workflow or script fix goes on `task/ci-…` → `develop`;
   - during a promotion, fix the release branch, then merge it into `main` again.

   Run the analyzer and tests locally before pushing. Then push and go back to step 1.
6. **Flaky runs:** for a failure that looks unrelated to the change (a network or runner error), re-run it once with `gh run rerun <id> --failed`. If it fails the same way twice, treat it as real.
7. **Stop after 3 fix attempts on the same failure,** and report: what failed, what you tried, and the log excerpt. Never push to `main` without a release.

## Step 6b: Release notes on every build

Whenever you make an App Store build (promote `release/x.y.z` → `main`, or run `tool/testflight.sh`), write that version's App Store "What's New" text first, and commit it on the release branch so it's kept with the version's history.

1. **What changed:** `git log --no-merges --oneline main..release/x.y.z` and the diff of `lib/` and the ARB files. Only claim what's in that diff.
2. **Locales:** read the version's localizations from the App Store Connect API (`/v1/appStoreVersions/<id>/appStoreVersionLocalizations`, signed with the key in `tool/asc.env`). Write one section per locale the store listing has; don't add locales it doesn't have.
3. **Write `release-notes/x.y.z.md`:** one `## <locale>` heading per locale, then the plain text to paste (no markdown inside it, since App Store Connect shows it raw). User-facing words only: no ticket codes, branch names, class names or "refactor". Under 4,000 characters per locale, which is App Store Connect's limit. Lead with the change users will notice most. Use the app's brand voice if the project has one.
4. **The first version has no notes:** App Store Connect has no What's New field for 1.0. Skip it, and say so.
5. **Notify the user:** send the file (SendUserFile, `proactive`), and paste each locale's text in chat in its own code block, so it can be copied in one go. Tell them where it goes: App Store Connect → the version → **What's New in This Version**.

## Step 7: Report back

- A branch table: name, commit, role.
- What's on GitHub, and the secrets that were checked.
- What saved where (`tool/asc.env`).
- How the first deploy happens: the next `release/x.y.z` merged into `main`, after a version bump. That first run is the first real CI test, and it gets watched as in Step 6.
- For every run you watched: its URL and result, and any fixes made.
- What isn't verified: the runner's Xcode and Flutter versions, and the key's signing rights until the first run.
- Leftovers: old feature branches to delete once `develop` is confirmed; uncommitted work you didn't take.

## Scope

Built for **Flutter iOS** apps. For a native iOS app, use the same steps without `flutter`: archive with `xcodebuild` directly. For Android or React Native, the branches and GitHub steps still apply, but CI needs its own build and upload, so say that's not covered rather than guessing.

## Files

| File | What it is |
|---|---|
| `RETRO.md` | The 7 Minute Math setup: what worked, what went wrong, and the fixes these rules come from |
| `templates/testflight.yml` | The GitHub Actions workflow (`__FLUTTER_VERSION__`) |
| `templates/testflight.sh` | The build-and-upload script, signed with the API key |
| `templates/ExportUpload.plist` | Export options for the upload (`__TEAM_ID__`) |
| `templates/asc.env` | The saved-answers file (git-ignored in the project) |
| `templates/README-infra.md` | The README sections: branches, flow, CI and secrets |
