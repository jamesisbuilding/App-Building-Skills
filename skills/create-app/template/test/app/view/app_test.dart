import 'package:__app__/app/app.dart';
import 'package:__app__/home/home.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:settings_repository/settings_repository.dart';

class _MockSettingsRepository extends Mock implements SettingsRepository {}

void main() {
  group(App, () {
    late SettingsRepository settingsRepository;

    setUp(() {
      settingsRepository = _MockSettingsRepository();
      when(
        () => settingsRepository.setAppearance(Appearance.dark),
      ).thenAnswer((_) async {});
    });

    testWidgets('shows the home page', (tester) async {
      await tester.pumpWidget(App(settingsRepository: settingsRepository));
      expect(find.byType(HomePage), findsOneWidget);
    });

    testWidgets('starts in the saved appearance', (tester) async {
      await tester.pumpWidget(
        App(
          settingsRepository: settingsRepository,
          appearance: Appearance.light,
        ),
      );
      final app = tester.widget<MaterialApp>(find.byType(MaterialApp));
      expect(app.themeMode, equals(ThemeMode.light));
    });

    testWidgets('switches theme when the appearance changes', (tester) async {
      await tester.pumpWidget(App(settingsRepository: settingsRepository));
      await tester.tap(find.text('Dark'));
      await tester.pumpAndSettle();
      final app = tester.widget<MaterialApp>(find.byType(MaterialApp));
      expect(app.themeMode, equals(ThemeMode.dark));
    });
  });
}
