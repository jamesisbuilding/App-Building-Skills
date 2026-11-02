---
name: new-app-info
description: Builds the information pack Apple asks for when App Review replies "We need additional information to better understand the app". It covers all six required items: (1) a screen recording on a physical device, as a shot list the user records; (2) the app's purpose and target audience; (3) setup and main features, with any login credentials or sample files; (4) the external services the app uses; (5) regional differences; (6) regulated industry or protected third-party material. It also runs Apple's "Prevent common issues" checks. Every answer comes from the app's own code (accounts, user-generated content, in-app purchases, SDKs, locales, screen-capture blocking, data deletion). It reads the connected iPhone's iOS version and checks it is the latest. It ends by telling the user to paste the reply into App Review Information → Notes. Use it when the user pastes that App Review message, says "/new-app-info", "we got rejected, they want more info", "answer App Review", or "make the App Store review pack". It writes app-store-assets/new-app-info.md (or ./new-app-info.md).
---

# new-app-info

Turn Apple's "we need additional information" request into one file. The user replies with it in App Store Connect and also pastes it into the Notes field of App Review Information, so future submissions have it. The recording is the one part only they can make.

## The six items Apple requires

Every pack answers all six, numbered 1–6 in this order, even if the user's message from Apple is missing or worded differently. If Apple's message adds or changes an item, follow Apple's version and note what was different.

| # | Apple asks for | Answered by |
|---|---|---|
| 1 | A screen recording captured on a physical device running the latest OS. It must begin with launching the app and show the typical user flow, including, where the app has them: account registration, login and account deletion; user-generated content with its reporting and blocking; and accessing paid content or features | Part 1 (the shot list) + reply §1 |
| 2 | The app's purpose and target audience: the problem it solves and the value it provides | Reply §2 |
| 3 | Instructions for setting up and accessing the main features, including any required login credentials or sample files | Reply §3 |
| 4 | The external services, tools or platforms used for core functionality (data providers, authentication, payment processors, AI services) | Reply §4 |
| 5 | Any regional differences in features or content, or confirmation that the app works the same in all regions | Reply §5 |
| 6 | For a highly regulated industry or protected third-party material: documentation or credentials showing authorisation | Reply §6 |

## Hard rules

1. **The recording must be from a physical device, on the latest OS, in one unedited take at normal speed, starting with tapping the app icon.** Never offer a simulator recording or a sped-up edit as the submission. You can't drive the user's phone, so the recording is theirs to make; your job is the shot list.
2. **Only claim what is in the build.** Every feature, service and language must come from the code, not from plans or notes.
3. **Not applicable is still an answer.** Give it in one sentence with the reason (e.g. "The app has no account registration or login").
4. **Accounts:** if users can create accounts, account deletion is required and must be in the recording; if it's missing, report that as a blocker. If there's a login, item 3 needs demo credentials (one set per account type): tell the user to enter them in App Store Connect. Never write real passwords into the file.
5. **Never send, submit or edit anything in App Store Connect.** The user pastes the reply and attaches the video.
6. Fill every placeholder you can from the repo or the device. List the ones left and what fills each one.

## Step 1: Read Apple's message

If the user pasted one, check its numbered items against the table above, and note which recording conditions (accounts, UGC, paid content) apply to this app.

## Step 2: Ground in the code

**Read the code at the submitted commit, not the working copy** (pin it first, as in Step 6 → The review build, step 0). The working copy is often a feature branch with unshipped features, and describing those to Apple is a claim about a build they don't have. Use `git grep <pattern> <commit> -- <paths>` and `git show <commit>:<path>`.

Exclude `build`, `Pods`, `.dart_tool`, `node_modules` and `.git` in every search.

| Item | Where to look |
|---|---|
| 1, 3: main flow from launch | Router and screens; onboarding; the core loop |
| 1, 3: accounts, login, deletion | `firebase_auth`, `sign_in_with_apple`, `supabase`, `Auth`, `login`, `signUp`, `deleteAccount`, `delete.*data` |
| 1: user-generated content | Posting, comments, chat, uploads; `report`, `block`, `flag` |
| 1, 3: paid content | `purchases_flutter`, `revenuecat`, `StoreKit`, `product_id`, paywall screens. Find which features are gated, any free tries, when the paywall can appear, and where Restore Purchases is |
| 1: screen-capture blocking | `no_screenshot`, `isSecureTextEntry` tricks, `UIScreen.capturedDidChange`, `FLAG_SECURE`. A blocked screen shows up blank in the recording, so the reply must say why |
| 2: purpose and audience | Store listing copy, brand or voice docs, README, launch checklist, onboarding copy (`.arb`, `.strings`, `strings.xml`) |
| 3: sample files | File imports, document pickers, QR/barcode scanning, hardware the app needs |
| 4: external services | Dependencies (`pubspec.yaml`, `Podfile`, `package.json`, Gradle) and build defines (`--dart-define`, keys files, release scripts). For each: what it does and what data it gets. Only list SDKs the release build actually turns on |
| 5: regions | Shipped locales; region checks (`locale`, `countryCode`, `region`); region-specific prices, features or content |
| 6: regulated or protected | Health, medical, finance, gambling, legal or kids content and claims; licensed content, music, images, fonts and their licences |
| Contact | Support emails in settings, privacy docs and website files |
| Platform | `IPHONEOS_DEPLOYMENT_TARGET`, `TARGETED_DEVICE_FAMILY` (iPhone only, or iPad too) |

Check that the analytics wording in item 4 matches the privacy policy in the repo. Flag it if it doesn't, or if you can't confirm the App Store Connect App Privacy answers.

## Step 3: The device and the OS (item 1)

1. `xcrun devicectl list devices` shows paired devices. Take the user's own iPhone that's available.
2. `xcrun devicectl device info details --device <id> | grep -i osVersion` shows its iOS version.
3. Search the web for the latest iOS release. If the phone is behind, say so: the user updates it in Settings → General → Software Update before recording, then you read the version again. The phone's OS is the user's to update.
4. If no phone is paired, leave `[iOS version]` and tell the user where to find it (Settings → General → About).

## Step 4: Prevent common issues

Check each of Apple's common issues, and put the result in the report back to the user. These are checks for the user, not part of the reply.

| Guideline | Check |
|---|---|
| 2.1 Bugs and crashes | The recording uses the TestFlight build of the submitted version, on a real device. Supported platforms from `TARGETED_DEVICE_FAMILY`: if iPad is supported, tell the user to test on an iPad too |
| 2.1 Accessing the app | Login → demo credentials are entered in App Store Connect, one set per account type, and still work |
| 2.3.3 Screenshots | List the store screenshots (e.g. `app-store-assets/*screenshots*`). Flag any that look like only title art, a splash or a login screen |
| 3.1.1 In-App Purchase | Every product id in the code is configured in App Store Connect and attached to this submission. List the ids for the user to check |
| 3.2 Other business models | If the app is for one business, organisation or its employees, flag that it needs a different distribution option (custom apps or unlisted distribution) |

## Step 5: Write the file

Write `app-store-assets/new-app-info.md` if that folder exists, else `./new-app-info.md`. Keep this shape (a full example is in `examples/seven-minute-math/new-app-info.md`):

```markdown
# App Review information — <App name>

Reply in App Store Connect with Part 2 and attach the recording. Then paste Part 2 into
App Review Information → Notes, so future submissions have it.
<Placeholders still to fill, if any.>

## Part 1 — the screen recording (item 1; record this yourself)
Why: a physical device, the latest OS, one take, normal speed, starting from tapping the icon.
Setup (default: a release build installed from the Mac; see "The review build" below):
create a sandbox tester (App Store Connect → Users and Access → Sandbox → Test Accounts);
delete the app from the phone; you build and install the review build; Screen Recording in
Control Centre with the mic off; Do Not Disturb on; sign in to Apple's purchase sheet with
the sandbox tester (the sheet saying "Sandbox" is expected).
Shot list, numbered: tap the icon → onboarding → the typical flow end to end → results →
every recording condition that applies (sign up, log in, delete the account; post, report,
block; paywall, sandbox purchase, the unlocked feature, Restore Purchases) → how users
delete their data → stop.
Any screen that will be blank (capture blocking) and why.

## Part 2 — the reply (paste this)
Greeting, plus the device and iOS version the recording was made on.
**1. Screen recording** … **6. Regulated industry / third-party material**: one bolded section each.
Closing line with the support email.
```

Writing:
- §1: what the recording shows, which recording conditions don't apply and why, and any blank screens.
- §2: who it's for, the problem, how the app solves it, the value. Three or four sentences.
- §3: what's needed to start (credentials go in App Store Connect, never in the file), then the main features in a short list, with free vs paid and when the paywall appears.
- §4: a bullet per service with what it does. Then one line saying what the app doesn't use (AI, data providers, auth), where that's true.
- §5: languages and any regional differences, or "works the same in every region".
- §6: documentation, or "Not applicable" with the reason.
- Plain, factual and polite. No marketing language.

## Step 6: The end-to-end video (item 1)

### The review build

Record a **release** build of **exactly the version that's in review**, installed on the phone straight from the Mac. You build and install it; the user records.

0. **Pin the submitted version.** Ask the user for the version and build number shown in App Store Connect for the submission in review (e.g. 1.0.0 (1)), unless they've already given it. Find the commit that produced it: a release tag, the release or main branch, a commit message such as "shipped to the App Store", or the commit where `pubspec.yaml`/`Info.plist` set that version and build. If two commits could match, ask which one. **Never build from the working copy:** it's often on a feature branch with uncommitted changes that Apple hasn't seen. Build in an isolated worktree instead (`git worktree add --detach <scratch>/review-build <commit>`). Copy any git-ignored key files (e.g. `keys.json`) into it with `cp`, without reading them. Tell the user which commit you're building and what's on newer branches that won't be in the video.
1. Find the project's normal device build (run scripts, `tool/*.sh`, Makefile, Fastlane). Remove every flag that fakes purchases, such as `DUMMY_PURCHASES`, `MOCK`, `FAKE`, `USE_TEST_STORE`, a RevenueCat `test_` key or a StoreKit configuration file. A fake purchase never shows Apple's sheet, and a reviewer seeing paid features unlock without it may treat that as a way around in-app purchase (3.1.1). Check that the purchase key is the live store key by its prefix only (e.g. `grep -q '"REVENUECAT_IOS_KEY": "appl_'`); never print key values.
2. Build in release mode, never debug: debug Flutter and React Native builds can't be opened from the home-screen icon, and Apple wants the recording to start there. Flutter: `flutter build ios --release` with the project's usual defines minus the fake ones.
3. **Check the built app matches the submission:** `/usr/libexec/PlistBuddy -c "Print CFBundleShortVersionString" -c "Print CFBundleVersion" build/ios/iphoneos/Runner.app/Info.plist` must print the submitted version and build. If it doesn't, stop and tell the user.
4. Ask the user to delete the app from the phone first (it erases their data on the phone, so it's their call), then install: `xcrun devicectl device install app --device <id> build/ios/iphoneos/Runner.app`.
5. Builds installed from the Mac buy through Apple's sandbox, so the user needs a sandbox tester to sign in to the purchase sheet. A TestFlight install of the same build number also works (purchases are free with their own Apple ID), and it guarantees the exact binary Apple has. Use it if the user prefers.

### Recording and checking

The pack isn't finished until the recording exists and has been checked. The user records it; you prompt them through it. In chat, give them Part 1's setup (including the sandbox tester) and the numbered shot list. Ask them to AirDrop the file into `app-store-assets/review-recording/` and tell you when it's there. Then:

1. `ffprobe -v error -show_entries format=duration:stream=width,height,codec_name -of default=nw=1 <file>`. Check that the resolution matches a real iPhone screen (not a simulator window or a cropped edit) and that the duration covers the whole flow.
2. Make a contact sheet with one frame every 10 seconds: `ffmpeg -i <file> -vf "fps=1/10,scale=240:-1,tile=8x8" -frames:v 1 <dir>/contact.png`. Also save the first frame on its own. Read both.
3. Check, in order: the first frame shows the home screen or the app icon being tapped; every shot-list step appears; there's no simulator chrome or editing, and no cuts. Also check that no notifications or personal data are visible. Tell the user anything that's missing and ask them to re-record; don't edit it yourself.
4. If the file is larger than App Store Connect allows, re-encode it at full length and normal speed, without trimming: `ffmpeg -i <file> -c:v libx264 -crf 28 -preset slow -an <dir>/<app>-review-recording.mp4`. Otherwise use it as it is.
5. Put the final path at the top of the pack file, as the attachment.

## Step 7: Report back

In chat, in this order:
1. Where the file is, and where the checked recording is (or that it's still to record).
2. The Part 2 reply, ready to paste.
3. The placeholders still open and what fills each one.
4. Blockers and risks: a missing account deletion, UGC without reporting or blocking, IAP products not attached, capture blocking, analytics that don't match the privacy policy, or a phone behind on iOS. Include the Step 4 results.
5. End with this prompt, always:

   > **Next:** record the video, then in App Store Connect reply to App Review with Part 2 and attach the recording. Then go to your app → the version → **App Review Information → Notes**, paste Part 2 there too and save, so Apple has it for every future submission.
