import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:storage_client/storage_client.dart';

class _MockPrefs extends Mock implements SharedPreferencesAsync {}

void main() {
  group(StorageClient, () {
    late SharedPreferencesAsync prefs;
    late StorageClient client;

    setUp(() {
      prefs = _MockPrefs();
      client = StorageClient(prefs: prefs);
    });

    test('read returns the stored string', () async {
      when(() => prefs.getString('key')).thenAnswer((_) async => 'value');
      expect(await client.read('key'), equals('value'));
    });

    test('write stores the string', () async {
      when(() => prefs.setString('key', 'value')).thenAnswer((_) async {});
      await client.write('key', 'value');
      verify(() => prefs.setString('key', 'value')).called(1);
    });
  });
}
