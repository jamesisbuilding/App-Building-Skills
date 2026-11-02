# __title__

Flutter app on Cubit/Bloc and a layered architecture. Keep this shape and follow these
rules for every change.

## Layers

UI → Cubit/Bloc → Repository → Data client. Dependencies point one way only; never skip
or invert a layer.

| Layer | Lives in | Example |
|---|---|---|
| Data: talks to one outside thing (API, storage, SDK). No app logic | `packages/<name>_client/` | `storage_client` |
| Repository: one per domain; turns data into app models | `packages/<name>_repository/` | `settings_repository` |
| Business logic: Cubit (or Bloc when you need event transforms) | `lib/<feature>/cubit/` | `AppearanceCubit` |
| Presentation: widgets only, no logic | `lib/<feature>/view/` | `AppearancePicker` |

- `lib/main.dart` is the only file that builds data clients and repositories, and the
  only file that imports a data package. `App` provides repositories with
  `RepositoryProvider`.
- Repositories take their data client in the constructor, never build one themselves,
  and never import another repository. Combine two repositories in a cubit.
- Data packages return typed response models (`fromJson`), never raw JSON, and throw
  typed exceptions.
- Domain models (like `Appearance`) live in the repository package and extend
  `Equatable` (enums excepted). Never let an API response shape reach a cubit.
- Flutter-only mapping (like `Appearance` → `ThemeMode`) lives in the feature's `view/`.
  Repository packages stay free of widgets.
- Local packages are `path:` dependencies. Every package and feature has a barrel
  file; import `appearance/appearance.dart`, never a file in `src/` or inside another
  feature.

## Features

```text
lib/<feature>/
├── <feature>.dart            # barrel
├── cubit/
│   ├── <feature>_cubit.dart
│   └── <feature>_state.dart
└── view/
    ├── <feature>_page.dart   # Page: BlocProvider creates the cubit
    └── <feature>_view.dart   # View: reads state, no logic
```

A feature with no state of its own (like `home`) has only `view/`. App-wide cubits
(like `AppearanceCubit`) are provided in `lib/app/view/app.dart`.

## Cubit / Bloc

- Cubit by default. Bloc only when you need events: debounce, restartable, a log of
  what happened.
- All business logic in cubits. Widgets only show state and forward taps.
- One cubit per feature concern. Cubits never depend on other cubits; they share a
  repository or the UI passes values between them.
- States and events extend `Equatable`. Several state types → a `sealed` class
  (`LoginInitial`, `LoginInProgress`, `LoginSuccess`, `LoginFailure`). One shape → a
  single class with a `status` enum and `copyWith`.
- Events are named subject + noun + past-tense verb: `LoginFormSubmitted`,
  `TodoListTodoDeleted`.
- `emit` only inside the method or handler that owns it, never from a callback that
  outlives it.
- `context.read` in callbacks, `context.select` / `BlocBuilder` in `build`.
  `BlocListener` for side effects (navigation, snackbars).

## Tests

- Tests mirror `lib/` (and each package's `lib/`). Run every suite before calling
  work done.
- Cubits: `blocTest` from `bloc_test`, with `build:` making a fresh cubit every time.
- Mocks: `mocktail` only. Declare them private per file:
  `class _MockX extends Mock implements X {}`.
- `group(ClassName, ...)` → `group('method', ...)` → a test name that reads as a
  sentence (`returns system when nothing is saved`). Never `'works'`.
- `setUp` and `tearDown` live inside a `group`; mutable objects are `late` and built
  in `setUp`. No state shared between tests.
- Widget tests: wrap with `tester.pumpApp`, mock cubits with `MockCubit`, prefer
  `find.byType` / `find.text`. Assert behaviour (shows, calls, navigates), not padding,
  colours or font sizes. Prefer `pump()` to `pumpAndSettle()`, which hangs on endless
  animations.

## Localization

- No hard-coded user-facing text. Add the string to `lib/l10n/arb/app_en.arb` with a
  `@description`, and use `context.l10n.<key>`.
- Reusable widgets take strings as parameters instead of reading `context.l10n`.
- Use `EdgeInsetsDirectional` and `start`/`end` alignment, not left/right, so
  right-to-left languages lay out correctly.

## Theming

- `ThemeData` is the only source of colours, text styles and component styles. Use
  `Theme.of(context).colorScheme` and `.textTheme`; no `Colors.x`, inline `TextStyle`,
  or `fontSize` inside `build`.
- Never branch on brightness in widgets. Light and dark are two `ColorScheme`s.
- Spacing comes from named constants on a base unit, not ad-hoc numbers.

## Accessibility

- Tappable things are buttons or `InkWell`, never a bare `GestureDetector`. Targets are
  at least 48×48.
- Icon-only buttons have a `tooltip`. Images have a `semanticLabel`, or
  `excludeFromSemantics: true` when decorative.
- Colour is never the only signal; pair it with text, an icon or a shape.
- No fixed-height boxes around text (it clips at large font sizes); use `minHeight`.
- Anything done by dragging also has a button.
- Text fields for email, password, name and so on set `autofillHints`.
- Async results that appear on screen are announced (`Semantics(liveRegion: true)`).

## Animations

- Simplest tool that works: implicit (`AnimatedOpacity`, `AnimatedContainer`,
  `AnimatedSwitcher`) before an `AnimationController`.
- Durations and curves come from Flutter's Material tokens (`Durations.medium2`,
  `Easing.standard`) or named constants, never inline numbers.
- Animate `Transform` and `Opacity`, not width, height or padding.
- Every controller is disposed. Respect `MediaQuery.disableAnimationsOf(context)`.

## Navigation

When the app gets a second screen, add `go_router`: nested routes for proper back
behaviour, `context.goNamed` over raw paths, `push` only when you need a result, never
`extra` (it breaks deep links), and hyphenated paths (`/weekly-report`).

## Security

- Real secrets never ship in the app, not even via `--dart-define` or `.env`: they're
  extractable from the binary. They belong behind a backend. Public SDK keys (like
  RevenueCat or Mixpanel) are fine.
- Tokens and personal data go in `flutter_secure_storage`, not `shared_preferences`.
- HTTPS only. No secrets or personal data in logs. `Random.secure()` for anything
  security-related.

## Checks

```bash
flutter analyze && flutter test
for p in packages/*/; do (cd "$p" && flutter test); done
```
