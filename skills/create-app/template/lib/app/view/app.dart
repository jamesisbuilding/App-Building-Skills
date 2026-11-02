import 'package:__app__/appearance/appearance.dart';
import 'package:__app__/home/home.dart';
import 'package:__app__/l10n/l10n.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:settings_repository/settings_repository.dart';

/// Provides the repositories and app-wide cubits, then builds [AppView].
class App extends StatelessWidget {
  const App({
    required SettingsRepository settingsRepository,
    this.appearance = Appearance.system,
    super.key,
  }) : _settingsRepository = settingsRepository;

  final SettingsRepository _settingsRepository;
  final Appearance appearance;

  @override
  Widget build(BuildContext context) {
    return RepositoryProvider.value(
      value: _settingsRepository,
      child: BlocProvider(
        create: (_) => AppearanceCubit(
          settingsRepository: _settingsRepository,
          initial: appearance,
        ),
        child: const AppView(),
      ),
    );
  }
}

class AppView extends StatelessWidget {
  const AppView({super.key});

  @override
  Widget build(BuildContext context) {
    final appearance = context.select<AppearanceCubit, Appearance>(
      (cubit) => cubit.state,
    );
    return MaterialApp(
      onGenerateTitle: (context) => context.l10n.appTitle,
      theme: ThemeData(colorSchemeSeed: Colors.indigo),
      darkTheme: ThemeData(
        colorSchemeSeed: Colors.indigo,
        brightness: Brightness.dark,
      ),
      themeMode: appearance.themeMode,
      localizationsDelegates: AppLocalizations.localizationsDelegates,
      supportedLocales: AppLocalizations.supportedLocales,
      home: const HomePage(),
    );
  }
}
