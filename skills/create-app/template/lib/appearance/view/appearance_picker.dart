import 'package:__app__/appearance/cubit/appearance_cubit.dart';
import 'package:__app__/l10n/l10n.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:settings_repository/settings_repository.dart';

class AppearancePicker extends StatelessWidget {
  const AppearancePicker({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = context.l10n;
    final appearance = context.select<AppearanceCubit, Appearance>(
      (cubit) => cubit.state,
    );
    return SegmentedButton<Appearance>(
      segments: [
        ButtonSegment(
          value: Appearance.system,
          label: Text(l10n.appearanceSystem),
        ),
        ButtonSegment(
          value: Appearance.light,
          label: Text(l10n.appearanceLight),
        ),
        ButtonSegment(
          value: Appearance.dark,
          label: Text(l10n.appearanceDark),
        ),
      ],
      selected: {appearance},
      onSelectionChanged: (selection) =>
          context.read<AppearanceCubit>().changed(selection.single),
    );
  }
}
