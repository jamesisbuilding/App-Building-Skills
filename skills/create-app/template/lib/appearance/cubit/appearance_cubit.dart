import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:settings_repository/settings_repository.dart';

/// Holds the chosen [Appearance] and saves changes through the repository.
class AppearanceCubit extends Cubit<Appearance> {
  AppearanceCubit({
    required SettingsRepository settingsRepository,
    Appearance initial = Appearance.system,
  }) : _settingsRepository = settingsRepository,
       super(initial);

  final SettingsRepository _settingsRepository;

  Future<void> changed(Appearance appearance) async {
    emit(appearance);
    await _settingsRepository.setAppearance(appearance);
  }
}
