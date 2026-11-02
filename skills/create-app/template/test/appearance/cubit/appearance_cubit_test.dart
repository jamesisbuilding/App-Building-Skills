import 'package:__app__/appearance/appearance.dart';
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:settings_repository/settings_repository.dart';

class _MockSettingsRepository extends Mock implements SettingsRepository {}

void main() {
  group(AppearanceCubit, () {
    late SettingsRepository settingsRepository;

    setUp(() {
      settingsRepository = _MockSettingsRepository();
      when(
        () => settingsRepository.setAppearance(any()),
      ).thenAnswer((_) async {});
    });

    setUpAll(() => registerFallbackValue(Appearance.system));

    test('starts with the initial appearance', () {
      expect(
        AppearanceCubit(
          settingsRepository: settingsRepository,
          initial: Appearance.dark,
        ).state,
        equals(Appearance.dark),
      );
    });

    blocTest<AppearanceCubit, Appearance>(
      'emits and saves the new appearance when changed',
      build: () => AppearanceCubit(settingsRepository: settingsRepository),
      act: (cubit) => cubit.changed(Appearance.light),
      expect: () => [Appearance.light],
      verify: (_) => verify(
        () => settingsRepository.setAppearance(Appearance.light),
      ).called(1),
    );
  });
}
