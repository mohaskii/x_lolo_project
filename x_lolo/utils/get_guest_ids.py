from typing import Dict, Optional
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs
from ..request_payload_and_headers import (
    GET_TOK_REQUEST_COMPONENTS,
    GET_IDS_COOKIES_REQUEST_COMPONENTS,
    GET_X_GUEST_TOKEN_REQUEST_COMPONENTS,
)
from http.cookies import SimpleCookie, BaseCookie
from ..cookie import Cookie
import re


def get() -> Cookie:
    response = requests.get(
        url=GET_TOK_REQUEST_COMPONENTS["url"],
        headers=GET_TOK_REQUEST_COMPONENTS["headers"],
    )
    if response.status_code != 200:
        raise Exception(
            "Error: Failed to retrieve guest IDs. Status code: {response.status_code}"
        )

    html_doc = response.text
    tok = retrieve_tok(html_doc)
    if tok is None:
        raise Exception(f"Error: {response.text}. Status code: {response.status_code}")
    response = requests.get(
        url=GET_IDS_COOKIES_REQUEST_COMPONENTS["url"](tok),
        headers=GET_IDS_COOKIES_REQUEST_COMPONENTS["headers"],
    )
    if response.status_code != 200:
        raise Exception(f"Error: {response.text}. Status code: {response.status_code}")

    return extract_cookies_trim(response.headers["set-cookie"])


def retrieve_tok(html_doc: str) -> Optional[str]:
    soup = BeautifulSoup(html_doc, "html.parser")
    meta_tag = soup.find("meta", attrs={"http-equiv": "refresh"})

    if meta_tag:
        content = meta_tag.get("content", "")
        url_part = content.split("url = ")[-1].strip()

        parsed_url = urlparse(url_part)
        query_params = parse_qs(parsed_url.query)

        tok_value = query_params.get("tok", [None])[0]
        if tok_value:
            return tok_value
    return None


def extract_cookies_trim(cookie_string: str) -> Cookie:

    cookies = SimpleCookie(cookie_string)

    cookies_to_return = {}

    for key, morsel in cookies.items():

        cookies_to_return[key] = morsel.value.lstrip("v1%3A")

    return Cookie(cookies_to_return)


def get_x_guest_token(cookies: Cookie) -> str:
    response = requests.get(
        url=GET_X_GUEST_TOKEN_REQUEST_COMPONENTS["url"],
        headers=GET_X_GUEST_TOKEN_REQUEST_COMPONENTS["headers"](cookies),
    )
    if response.status_code != 200:
        raise Exception(f"Error: {response.text}. Status code: {response.status_code}")

    html_doc = response.text
    return retrieve_x_guest_token_value_from_html_response(html_doc)


def retrieve_x_guest_token_value_from_html_response(html_doc: str) -> str:
    soup = BeautifulSoup(html_doc, "html.parser")
    script_tags = soup.findAll("script")
    token = ""
    for script in script_tags:
        if script.string and script.string.strip().startswith("document.cookie="):
            token = re.search(r"gt=([\d]+)", script.string).group(1)
            break

    return token
