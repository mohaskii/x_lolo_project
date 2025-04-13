import 'package:http/http.dart' as http;
import 'package:x_lolo/src/const/payload_and_headers.dart';
import 'package:html/parser.dart' show parse;
import 'package:html/dom.dart';
import 'dart:convert';

class Cookie {
  final Map<String, String> dict;
  Cookie({required this.dict});
  String encode() =>
      dict.entries.map((entry) => "${entry.key}=${entry.value}").join("; ");
}

class Session {
  late final Cookie cookie;
  late final String guestToken;
  late final String flowToken;

  // Make the constructor async
  Future<void> initialize() async {
    cookie = (await getGuestIDandCookies());
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
}

Future<Cookie> getGuestIDandCookies() async {
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
  return Cookie(dict: extractCookiesTrim(cookies));
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

String getAtt(String cookieString) {
  final List<String> parts = cookieString.split('; ');

  for (String part in parts) {
    // Split each part by '='
    if (part.toLowerCase().startsWith("expires")) {
      continue;
    }
    final int equalsIndex = part.indexOf('=');
    if (equalsIndex == -1) continue;

    String value = part.substring(equalsIndex + 1);
    final subCookies = value.split(',');
    if (subCookies.length == 1) {
      continue;
    }
    subCookies.removeAt(0);
    final cookie = getCookie(subCookies[0]);
    if (cookie.$1 == "att") return cookie.$2;
  }
  throw Exception(
      'Unable to find "att" cookie in the response. Cookie string: $cookieString');
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
  // print("${guestToken}...${cookie.encode()}");
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
    attCookie: getAtt(response.headers["set-cookie"]!)
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

  final cookie = extractCookiesTrim(response.headers["set-cookie"]!);

  print(cookie);
}


