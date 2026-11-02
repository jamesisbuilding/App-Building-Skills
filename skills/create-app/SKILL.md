---
name: create-app
description: Initialises a new Flutter app with our house structure. It runs flutter create (iOS + Android, com.<app> bundle ID, personal signing team), then lays down a Cubit/Bloc app on a four-layer architecture (data client package → repository package → Cubit → view) with a working example through every layer, localization wired in, very_good_analysis + bloc_lint, mocktail/bloc_test tests that mirror lib/, and a CLAUDE.md describing the rules. It finishes by running analyze and every test suite. Use it when the user says "/create-app", "create a new app", "start a new Flutter app", "init a new app", "scaffold an app like we do" or "new project for <idea>".
---

# create-app

Create a new Flutter app with the structure every app of ours shares. Run it before
`app-set-up-infra`. The new project's `CLAUDE.md` carries the best-practice rules
(architecture, Cubit, tests, localization, theming, accessibility, animations,
navigation, security), so every later session follows them. They're condensed from Very
Good Ventures' MIT-licensed skills (see `LICENSE-VGV`).

## What it builds

```text
<app>/
├── CLAUDE.md                     # structure + best-practice rules, for future sessions
├── lib/
│   ├── main.dart                 # builds data clients + repositories, BlocObserver, runApp
│   ├── app/view/app.dart         # RepositoryProvider + app-wide cubits + MaterialApp
│   ├── appearance/               # example feature: cubit/ + view/ + barrel
│   ├── home/view/home_page.dart
│   └── l10n/                     # app_en.arb + context.l10n
├── packages/
│   ├── storage_client/           # data layer: shared_preferences wrapper
│   └── settings_repository/      # repository layer: Appearance setting
└── test/                         # mirrors lib/, plus helpers/pump_app.dart
```

The example (pick system/light/dark, saved across launches) is real: most apps keep it.
It shows the whole path: `AppearancePicker` → `AppearanceCubit` → `SettingsRepository`
→ `StorageClient` → device.

Not included, on purpose: flavors, routing, analytics, purchases, CI. Add go_router when
there's a second screen (rules in the project's `CLAUDE.md`). CI and branches come from
`app-set-up-infra`.

## Steps

1. **Get the names.** Ask only for what the request doesn't give you:
   - the project name in snake_case (`habit_tracker`). It becomes the Dart package and
     the bundle ID (`com.habitTracker`).
   - the display title (`Habit Tracker`), shown on the home screen and in the app bar.
   - the parent folder. Default: the current working directory.

   Don't ask about state management, architecture or packages. Those are fixed.

2. **Run the scaffold** (in the background, since it takes a few minutes):

   ```bash
   ~/.claude/skills/create-app/scripts/scaffold.sh <snake_name> "<Title>" "<parent_dir>" 382K295FY6
   ```

   `382K295FY6` is the personal paid Apple team. Always pass it: without it, flutter
   create picks Xcode's first team, which can be a work team.

   The script stops on the first error. It ends with `OK: <path>` only once
   `flutter analyze` is clean and the app and both package test suites pass.

3. **If it fails**, fix the cause in this skill's `template/` (or `scripts/`), not only in
   the new project, so the next app doesn't hit it. Then delete the half-made project and
   run it again.

4. **Report** the path, the bundle ID, and that analyze and tests are green. Suggest the
   next steps: rename the example `home` to the app's first real screen, and run
   `app-set-up-infra` for git, GitHub and TestFlight.

## Keeping the template current

- Versions aren't pinned in `template/`. The script uses `flutter pub add`, so every app
  gets the latest versions that work with the installed Flutter.
- `dart fix --apply` runs after the copy. It sorts imports for the real package name and
  applies newer-Dart lint fixes, so template code can stay in the classic style.
- When a structure or rule changes in a real app and it's worth keeping, change
  `template/` and `template/CLAUDE.md` to match.
