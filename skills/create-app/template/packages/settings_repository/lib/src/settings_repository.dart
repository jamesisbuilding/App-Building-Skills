import 'package:storage_client/storage_client.dart';

/// How the app picks light or dark mode.
enum Appearance {
  /// Follow the phone's setting.
  system,

  /// Always light.
  light,

  /// Always dark.
  dark,
}

/// The user's app settings.
class SettingsRepository {
  /// Creates a [SettingsRepository] that keeps settings in [storage].
  const SettingsRepository({required StorageClient storage})
    : _storage = storage;

  final StorageClient _storage;

  static const _appearanceKey = 'appearance';

  /// The saved appearance, or [Appearance.system] if none is saved.
  Future<Appearance> appearance() async {
    final name = await _storage.read(_appearanceKey);
    return Appearance.values.asNameMap()[name] ?? Appearance.system;
  }

  /// Saves [appearance].
  Future<void> setAppearance(Appearance appearance) =>
      _storage.write(_appearanceKey, appearance.name);
}
