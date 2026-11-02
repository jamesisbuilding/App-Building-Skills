import 'package:flutter/material.dart';
import 'package:settings_repository/settings_repository.dart';

// The repository stays Flutter-free, so the mapping to ThemeMode lives here
extension AppearanceThemeMode on Appearance {
  ThemeMode get themeMode => switch (this) {
    Appearance.system => ThemeMode.system,
    Appearance.light => ThemeMode.light,
    Appearance.dark => ThemeMode.dark,
  };
}
