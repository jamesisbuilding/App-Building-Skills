# Retro: 7 Minute Math infra setup (2026-10-31)

Setting up branches, GitHub and TestFlight CI for 7 Minute Math, while 1.0.0 was in App Review. This file records what happened, what went wrong and what the skill now does about it.

## What we ended with

- **Branches:**
  - `main` (prod) and `release/1.0.0` (version history), both at the shipped commit.
  - `develop`, holding all feature work merged.
  - `feat/` / `fix/` / `task/` branches from `develop` for new work.
- **GitHub:** `jamesisbuilding/sevenminutemath`, private, `main` as the default branch.
- **CI:** `.github/workflows/testflight.yml`, which on every push to `main` runs the tests, then `tool/testflight.sh`, and uploads to TestFlight. Signing is automatic through an App Store Connect API key, so there's no fastlane match and no certificates repo.
- **Secrets:** `KEYS_JSON`, `ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_KEY_P8`. The user set them; Claude checked them by listing their names only.
- **Local config:** `tool/asc.env` (git-ignored) holds the key ID, issuer ID, key path and repo.

## What went well

- **Reusing the project's own upload script.** `tool/testflight.sh` already signed with the API key. Wrapping it in CI was simpler than porting GetAhead's fastlane and match setup.
- **Merging into `develop` in a separate worktree.** The shared working copy was never checked out or reset.
- **Conflicts resolved by reading both sides.** All of them were additive, so both sides were kept. The analyzer and tests were run after each merge.
- **Comparing features before merging an old branch.** `wip/w0-honesty-combined` was an earlier copy of work that later branches had redone. A count of each feature on both sides showed this, so it was recorded as merged without bringing its changes in.
- **Keeping CI off `main` while 1.0.0 was in review.** Pushing it straight to `main` would have uploaded another 1.0.0 build.

## What went wrong, and the fix

| What happened | Fix in the skill |
|---|---|
| The first device build came from the working copy: a feature branch with 40 uncommitted files, not the shipped version. | Pin the commit for anything tied to a release, and build it in a worktree. |
| `tool/phone.sh` builds with `DUMMY_PURCHASES=true`, which fakes purchases, so Apple's sheet never appears. | Look for fake-purchase flags in device scripts, and note them in the README. |
| The issuer ID was assumed to be in `keys/`. A `.p8` holds only the private key; the issuer ID exists only in App Store Connect. | Ask for it with AskUserQuestion, and say where to find it. |
| `git remote add` failed: the remote had already been added and pushed, by the user or another session. | Check `git remote -v` and the remote branches before adding or pushing. |
| GetAhead's workflow calls a template in a client org (`Better-Design-Digital`). Reading it needed a switch of GitHub accounts, which was blocked. | Never depend on another org's template. Write a standalone workflow. |
| Uncommitted work could have belonged to a live session. | Before committing someone else's work, check the file edit times and run the analyzer and tests. |
| `testflight.sh` could fail an export or upload and still exit 0. | `setopt pipefail` in the script. |
| An analyzer warning came out of a merge (a lost `@override`). | Analyzer plus tests after every merge, with a fix-up commit. |

## Still not verified

- ~~The first CI run~~ **Verified 2026-10-31:** a dummy `release/1.0.1` (the shipped code plus the CI commit plus a version bump) was promoted to `main`. Run 41196203070 went green on the first try in about 7 minutes: Flutter 3.44.6 stable and the latest Xcode on `macos-26`, the tests, archive and export, and "Upload succeeded" to TestFlight. The API key signed on a fresh runner. `main` was then merged back into `develop`.
- Branch protection isn't available for private repos on GitHub Free, so the flow depends on discipline rather than rules.
