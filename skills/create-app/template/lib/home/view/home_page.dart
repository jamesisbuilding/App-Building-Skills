import 'package:__app__/appearance/appearance.dart';
import 'package:__app__/l10n/l10n.dart';
import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(context.l10n.appTitle)),
      body: const Center(child: AppearancePicker()),
    );
  }
}
