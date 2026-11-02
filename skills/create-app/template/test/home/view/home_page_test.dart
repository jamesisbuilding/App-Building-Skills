import 'package:__app__/appearance/appearance.dart';
import 'package:__app__/home/home.dart';
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:settings_repository/settings_repository.dart';

import '../../helpers/helpers.dart';

class _MockAppearanceCubit extends MockCubit<Appearance>
    implements AppearanceCubit {}

void main() {
  group(HomePage, () {
    testWidgets('shows the appearance picker', (tester) async {
      final cubit = _MockAppearanceCubit();
      when(() => cubit.state).thenReturn(Appearance.system);
      await tester.pumpApp(
        BlocProvider<AppearanceCubit>.value(
          value: cubit,
          child: const HomePage(),
        ),
      );
      expect(find.byType(AppearancePicker), findsOneWidget);
    });
  });
}
