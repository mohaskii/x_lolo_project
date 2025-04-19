import 'package:test/test.dart';
import 'package:x_lolo/src/session.dart';
  
void main() {
  group('Cookie and Token Tests', () {
    test('getGuestIDandCookies returns a Cookie object', () async {
      final session = Session();
      await session.initialize();
      final cookie = session.cookie;

      expect(cookie, isNotNull);
      expect(cookie, isA<Cookie>());
      expect(cookie.dict, isA<Map<String, String>>());
      expect(cookie.dict.isNotEmpty, true);

      // Check if it contains expected cookie keys
    });

    test('getGuestToken returns a token string', () async {
      // First get a cookie to use
      final session = Session();
      await session.initialize();

      // Then test getGuestToken
      final token = session.guestToken;

      expect(token, isNotNull);
      expect(token, isA<String>());
      expect(token.isNotEmpty, true);

      // Guest tokens are usually numeric
      print('Guest token: $token');
      expect(int.tryParse(token), isNotNull);
    });
  });
}
