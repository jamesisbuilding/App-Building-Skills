import 'dart:developer';

import 'package:__app__/app/app.dart';
import 'package:bloc/bloc.dart';
import 'package:flutter/widgets.dart';
import 'package:settings_repository/settings_repository.dart';
import 'package:storage_client/storage_client.dart';

/// The one place that builds data clients and repositories and wires them in.
/// Only this file imports data packages; everything else goes through a
/// repository.
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  FlutterError.onError = (details) {
    log(details.exceptionAsString(), stackTrace: details.stack);
  };
  Bloc.observer = const AppBlocObserver();

  // Data layer
  final storageClient = StorageClient();

  // Repository layer
  final settingsRepository = SettingsRepository(storage: storageClient);

  // Read before the first frame so a dark-mode user never sees a light flash
  final appearance = await settingsRepository.appearance();

  runApp(App(settingsRepository: settingsRepository, appearance: appearance));
}

class AppBlocObserver extends BlocObserver {
  const AppBlocObserver();

  @override
  void onChange(BlocBase<dynamic> bloc, Change<dynamic> change) {
    super.onChange(bloc, change);
    log('onChange(${bloc.runtimeType}, $change)');
  }

  @override
  void onError(BlocBase<dynamic> bloc, Object error, StackTrace stackTrace) {
    log('onError(${bloc.runtimeType}, $error, $stackTrace)');
    super.onError(bloc, error, stackTrace);
  }
}
