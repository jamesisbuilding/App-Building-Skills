import 'package:__app__/appearance/appearance.dart';
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:settings_repository/settings_repository.dart';

import '../../helpers/helpers.dart';

class _MockAppearanceCubit extends MockCubit<Appearance>
    implements AppearanceCubit {}

void main() {
  group(AppearancePicker, () {
    late AppearanceCubit cubit;

    setUp(() {
      cubit = _MockAppearanceCubit();
      when(() => cubit.state).thenReturn(Appearance.system);
      when(() => cubit.changed(Appearance.dark)).thenAnswer((_) async {});
    });

    Future<void> pump(WidgetTester tester) => tester.pumpApp(
      BlocProvider.value(value: cubit, child: const AppearancePicker()),
    );

    testWidgets('marks the current appearance as selected', (tester) async {
      await pump(tester);
      final button = tester.widget<SegmentedButton<Appearance>>(
        find.byType(SegmentedButton<Appearance>),
      );
      expect(button.selected, equals({Appearance.system}));
    });

    testWidgets('changes the appearance when an option is tapped', (
      tester,
    ) async {
      await pump(tester);
      await tester.tap(find.text('Dark'));
      verify(() => cubit.changed(Appearance.dark)).called(1);
    });
  });

  group('AppearanceThemeMode', () {
    test('maps every appearance to a theme mode', () {
      expect(Appearance.system.themeMode, equals(ThemeMode.system));
      expect(Appearance.light.themeMode, equals(ThemeMode.light));
      expect(Appearance.dark.themeMode, equals(ThemeMode.dark));
    });
  });
}
