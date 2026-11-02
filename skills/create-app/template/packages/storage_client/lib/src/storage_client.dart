import 'package:shared_preferences/shared_preferences.dart';

/// Reads and writes plain values on the device.
///
/// Knows nothing about the app: repositories decide what the keys mean.
class StorageClient {
  /// Creates a [StorageClient] backed by [prefs].
  StorageClient({SharedPreferencesAsync? prefs})
    : _prefs = prefs ?? SharedPreferencesAsync();

  final SharedPreferencesAsync _prefs;

  /// Returns the string stored under [key], or null if there is none.
  Future<String?> read(String key) => _prefs.getString(key);

  /// Stores [value] under [key].
  Future<void> write(String key, String value) => _prefs.setString(key, value);
}
