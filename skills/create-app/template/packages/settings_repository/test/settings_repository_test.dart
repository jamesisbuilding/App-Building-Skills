import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:settings_repository/settings_repository.dart';
import 'package:storage_client/storage_client.dart';

class _MockStorageClient extends Mock implements StorageClient {}

void main() {
  group(SettingsRepository, () {
    late StorageClient storage;
    late SettingsRepository repository;

    setUp(() {
      storage = _MockStorageClient();
      repository = SettingsRepository(storage: storage);
    });

    group('appearance', () {
      test('returns the saved appearance', () async {
        when(() => storage.read('appearance')).thenAnswer((_) async => 'dark');
        expect(await repository.appearance(), equals(Appearance.dark));
      });

      test('returns system when nothing is saved', () async {
        when(() => storage.read('appearance')).thenAnswer((_) async => null);
        expect(await repository.appearance(), equals(Appearance.system));
      });

      test('returns system when the saved value is unknown', () async {
        when(() => storage.read('appearance')).thenAnswer((_) async => 'neon');
        expect(await repository.appearance(), equals(Appearance.system));
      });
    });

    test('setAppearance saves the name', () async {
      when(() => storage.write('appearance', 'light')).thenAnswer((_) async {});
      await repository.setAppearance(Appearance.light);
      verify(() => storage.write('appearance', 'light')).called(1);
    });
  });
}
