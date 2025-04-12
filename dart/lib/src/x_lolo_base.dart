import 'package:http/http.dart' as http;
import 'package:x_lolo/src/const/payload_and_headers.dart';

class Cookie {
  final Map<String, String> dict;
  Cookie({required this.dict});
  String encode() =>
      dict.entries.map((entry) => "${entry.key}=${entry.value}").join("; ");

  // set dicts(Map<String, String> a) => dict = a;
}

class Session {
  final Cookie cookie;
  final String guestToken;
  Session(this.guestToken, this.cookie);

  // Session.fromYaml(dynamic data) {
  //   this.cookie = data["Cookie"];
  // }
}

Future<Cookie?> getGuestID() async {
  try {
    final url = Uri.parse(GET_TOK_REQUEST_COMPONENTS['url'].toString());
    final headers =
        GET_TOK_REQUEST_COMPONENTS["headers"] as Map<String, String>;
    final response = await http.get(url, headers: headers);
    if (response.statusCode != 200) {
      print("Error: Status code ${response.statusCode}");
      return null;
    }
    // Extract cookies from response headers
    final String? cookies = response.headers['set-cookie'];
    if (cookies == null || cookies.isEmpty) {
      print("No cookies found in response");
      return null;
    }
    final Cookie cookie = Cookie(dict: extractCookiesTrim(cookies));
    // print(cookie.dict);
    getGuestToken(cookie);
    return cookie;
  } catch (e) {
    print("Exception occurred: $e");
    return null;
  }
}

Future<Cookie?> getGuestToken(Cookie cookie) async {
  try {
    final url =
        Uri.parse(GET_X_GUEST_TOKEN_REQUEST_COMPONENTS['url'].toString());
    final Map<String, String> headers =
        (GET_X_GUEST_TOKEN_REQUEST_COMPONENTS["headers"] as Function)(cookie);

    final response = await http.get(url, headers: headers);
    if (response.statusCode != 200) {
      print("Error: Status code ${response.statusCode}");
      return null;
    }
    print(response.body);
    return null;
  } catch (e) {
    print("Exception occurred: $e");
    return null;
  }
}

void main() {
  getGuestID();
}

Map<String, String> extractCookiesTrim(String cookieString) {
  // Parse the cookie string
  final Map<String, String> cookiesToReturn = {};

  // Split the cookie string by semicolons
  final List<String> parts = cookieString.split('; ');

  for (String part in parts) {
    // Split each part by '='
    final int equalsIndex = part.indexOf('=');
    if (equalsIndex > 0) {
      final String key = part.substring(0, equalsIndex);
      String value = part.substring(equalsIndex + 1);

      // Similar to the Python lstrip("v1%3A")
      if (value.startsWith("v1%3A")) {
        value = value.substring(5); // Remove "v1%3A" prefix
      }

      cookiesToReturn[key] = value;
    }
  }

  return cookiesToReturn;
}
