import 'package:http/http.dart' as http;
import 'package:x_lolo/src/const/payload_and_headers.dart';
import 'package:html/parser.dart' show parse;
import 'package:html/dom.dart';
import 'dart:convert';
import 'package:x_lolo/src/post.dart';

class Cookie {
  final Map<String, String> dict;
  Cookie({required this.dict});
  String encode() =>
      dict.entries.map((entry) => "${entry.key}=${entry.value}").join("; ");
}

class Session {
  late Cookie cookie;
  late String guestToken;
  late String flowToken;
  late String xCsrfToken;
  late String userID;
  late String expire;
  // Make the constructor async
  Future<void> initialize() async {
    final data = await getGuestIDandCookies();
    cookie = Cookie(dict: data.cookies);
    expire = data.expires;
    guestToken = (await getGuestToken(cookie));
  }

  Future<void> login(
      String usernameOrEmail, String passWord, bool saveSession) async {
    final data = await getAuthFlows(cookie, guestToken);
    cookie.dict["att"] = data.attCookie;
    flowToken = data.flowToken;

    await passNextLink(this);
    await submitUsername(this, usernameOrEmail);
    await submitPassword(this, passWord);
  }

  Future<Post> addPost(String text, {String? mediaUrl = null}) async {
    // print(jsonEncode((textPostRequestComponents['payload'] as Function)(text)));§
    final response = await http.post(
        Uri.parse(textPostRequestComponents['url'] as String),
        headers: (textPostRequestComponents['headers'] as Function)(this),
        body: jsonEncode(
            (textPostRequestComponents['payload'] as Function)(text)));

    if (response.statusCode != 200) {
      throw Exception(
          'Failed to add post. Status code: ${response.statusCode}. Response body: ${response.body}');
    }

    return Post();
  }
}

Future<({Map<String, String> cookies, String expires})>
    getGuestIDandCookies() async {
  final response = await http.get(
      Uri.parse(getTokRequestComponents['url'].toString()),
      headers: getTokRequestComponents["headers"] as Map<String, String>);

  if (response.statusCode != 200) {
    throw Exception(
        'Failed to get guest ID. Status code: ${response.statusCode}. Response body: ${response.body}');
  }
  // Extract cookies from response headers
  final String? cookies = response.headers['set-cookie'];
  if (cookies == null || cookies.isEmpty) {
    throw Exception(
        'No cookies found in response. Response headers: ${response.headers}');
  }
  return getCookies(cookies);
}

String retrieveXGuestTokenValue(String htmlDoc) {
  // Parse HTML document
  Document document = parse(htmlDoc);

  // Find all script tags
  List<Element> scriptTags = document.getElementsByTagName('script');

  String token = "";

  for (Element script in scriptTags) {
    String scriptContent = script.text.trim();

    // Check if script content starts with "document.cookie="
    if (scriptContent.startsWith("document.cookie=")) {
      // Extract token using regex
      final tokenMatch = RegExp(r'gt=([\d]+)').firstMatch(scriptContent);
      if (tokenMatch != null) {
        token = tokenMatch.group(1) ?? "";
        break;
      }
    }
  }

  return token;
}

Future<String> getGuestToken(Cookie cookie) async {
  final response = await http.get(
      Uri.parse(getXGuestTokenRequestComponents['url'].toString()),
      headers:
          (getXGuestTokenRequestComponents["headers"] as Function)(cookie));
  if (response.statusCode != 200) {
    throw Exception(
        'Failed to get guest token. Status code: ${response.statusCode}. Response body: ${response.body}');
  }

  return retrieveXGuestTokenValue(response.body);
}

(String, String) getCookie(String part) {
  final int equalsIndex = part.indexOf('=');
  if (equalsIndex > 0) {
    final String key = part.substring(0, equalsIndex);
    String value = part.substring(equalsIndex + 1);

    // Similar to the Python lstrip("v1%3A")
    if (value.startsWith("v1%3A")) {
      value = value.substring(5); // Remove "v1%3A" prefix
    }
    return (key, value);
  }

  return throw Exception('Unable to get cookie. Invalid cookie part: $part');
}

({Map<String, String> cookies, String expires}) getCookies(
    String cookieString) {
  final Map<String, String> cookies = {};
  String? expires;
  final List<String> parts = cookieString.split('; ');
  final toIgnore = [
    "max-age",
    "expires",
    "path",
    "domain",
    "samesite",
  ];
  for (String part in parts) {
    if (part.toLowerCase().startsWith("expires")) {
      final cookie = getCookie(part);
      expires = cookie.$2;

      continue;
    }
    final int equalsIndex = part.indexOf('=');
    if (equalsIndex == -1) {
      continue;
    }

    final subCookies = part.split(',');
    if (subCookies.length == 1) {
      final cookie = getCookie(part);

      if (toIgnore.contains(cookie.$1.toLowerCase()) || cookie.$2.isEmpty) {
        continue;
      }
      cookies[cookie.$1] = cookie.$2;

      continue;
    }

    if (subCookies[0].contains('=')) {
      final cookie = getCookie(subCookies[0]);
      cookies[cookie.$1] = cookie.$2;
    }

    final cookie = getCookie(subCookies[1]);
    if (toIgnore.contains(cookie.$1.toLowerCase()) || cookie.$2.isEmpty) {
      continue;
    }
    cookies[cookie.$1] = cookie.$2;
  }

  return (cookies: cookies, expires: expires!);
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

Future<({String flowToken, String attCookie})> getAuthFlows(
    Cookie cookie, String guestToken) async {
  final response = await http.post(
      Uri.parse(getFlowTokenRequestComponents["url"] as String),
      headers: (getFlowTokenRequestComponents["headers"] as Function)(
          cookie, guestToken),
      body: jsonEncode(getFlowTokenRequestComponents['payload']));

  if (response.statusCode != 200) {
    throw Exception(
        'Failed to get auth flows. Status code: ${response.statusCode}. Response body: ${response.body}');
  }
  final Map<String, dynamic> responseJson = jsonDecode(response.body);
  final String flowToken = responseJson["flow_token"];

  return (
    flowToken: flowToken.substring(0, flowToken.length - 1),
    attCookie: getCookies(response.headers["set-cookie"]!).cookies['att']!
  );
}

Future<void> passNextLink(Session sess) async {
  final response = await http.post(
      Uri.parse(passNextLinkRequestComponents['url'] as String),
      headers: (passNextLinkRequestComponents['headers'] as Function)(
          sess.cookie, sess.guestToken),
      body: jsonEncode((passNextLinkRequestComponents['payload']
          as Function)(sess.flowToken)));

  if (response.statusCode != 200) {
    throw Exception(
        'Failed to pass next link. Status code: ${response.statusCode}. Response body: ${response.body}');
  }
}

Future<void> submitUsername(Session sess, String username) async {
  final response = await http.post(
      Uri.parse(submitUsernameRequestComponents['url'] as String),
      headers: (submitUsernameRequestComponents['headers'] as Function)(
          sess.cookie, sess.guestToken),
      body: jsonEncode((submitUsernameRequestComponents['payload'] as Function)(
          sess.flowToken, username)));

  if (response.statusCode != 200) {
    throw Exception(
        'Failed to submit username. Status code: ${response.statusCode}. Response body: ${response.body}');
  }
}

Future<void> submitPassword(Session sess, String password) async {
  final response = await http.post(
      Uri.parse(submitPasswordRequestComponents['url'] as String),
      headers: (submitPasswordRequestComponents['headers'] as Function)(
          sess.cookie, sess.guestToken),
      body: jsonEncode((submitPasswordRequestComponents['payload'] as Function)(
          sess.flowToken, password)));

  if (response.statusCode != 200) {
    throw Exception(
        'Failed to submit password. Status code: ${response.statusCode}. Response body: ${response.body}');
  }

  final cookies = getCookies(response.headers["set-cookie"]!).cookies;

  sess.cookie.dict["auth_token"] = cookies["auth_token"]!;
  sess.cookie.dict["ct0"] = cookies["ct0"]!;
  sess.userID = cookies["twid"]!.replaceAll('"u=', '').replaceAll('"', "");
  sess.xCsrfToken = cookies["ct0"]!;
}
