from ..request_payload_and_headers import (
    GET_FLOW_TOKEN_REQUEST_COMPONENTS,
    PASS_NEXT_LINK_REQUEST_COMPONENTS,
    SUBMIT_USERNAME_REQUEST_COMPONENTS,
    SUBMIT_PASSWORD_REQUEST_COMPONENTS,
)
from ..cookie import Cookie
from typing import Tuple
from http.cookies import SimpleCookie, BaseCookie
import re

import requests


def extract_cookies(cookie_string: str) -> Cookie:

    cookies = SimpleCookie(cookie_string)

    cookies_to_return = {}

    for key, morsel in cookies.items():

        cookies_to_return[key] = morsel.value

    return Cookie(cookies_to_return)


def get(cookie: Cookie, guest_token) -> Tuple[str, str]:
    response = requests.post(
        url=GET_FLOW_TOKEN_REQUEST_COMPONENTS["url"],
        headers=GET_FLOW_TOKEN_REQUEST_COMPONENTS["headers"](cookie, guest_token),
        json=GET_FLOW_TOKEN_REQUEST_COMPONENTS["payload"],
    )
    if response.status_code != 200:
        raise Exception(f"Error: {response.text}. Status code: {response.status_code}")
    cookies = response.headers["set-cookie"]
    cookies = extract_cookies(cookies)
    response = response.json()
    print()
    return (response["flow_token"].strip("0"), cookies.dict["att"])


def pass_next_link(sess):

    response = requests.post(
        url=PASS_NEXT_LINK_REQUEST_COMPONENTS["url"],
        headers=PASS_NEXT_LINK_REQUEST_COMPONENTS["headers"](
            sess.cookies, sess.x_guest_token
        ),
        json=PASS_NEXT_LINK_REQUEST_COMPONENTS["payload"](sess.flow_token),
    )
    if response.status_code != 200:
        raise Exception(f"Error: {response.text}. Status code: {response.status_code}")
    response_json = response.json()


def cookie_to_dict(cookie_string):
    # Séparer les cookies individuels
    cookies = cookie_string.split(", ")

    # Dictionnaire pour stocker les résultats
    cookie_dict = {}

    # Expression régulière pour trouver les paires clé=valeur
    pattern = re.compile(r"(\w+)=([^;]*)")

    for cookie in cookies:
        # Trouver la première paire clé=valeur dans chaque cookie
        match = pattern.match(cookie)
        if match:
            key = match.group(1)
            # Retirer les guillemets autour des valeurs si présents
            value = match.group(2).strip('"')
            cookie_dict[key] = value

    return cookie_dict


def submit_username(sess, username: str):
    response = requests.post(
        url=SUBMIT_USERNAME_REQUEST_COMPONENTS["url"],
        headers=SUBMIT_USERNAME_REQUEST_COMPONENTS["headers"](
            sess.cookies, sess.x_guest_token
        ),
        json=SUBMIT_USERNAME_REQUEST_COMPONENTS["payload"](sess.flow_token, username),
    )
    if response.status_code != 200:
        raise Exception(f"Error: {response.text}. Status code: {response.status_code}")
    response_json = response.json()
    flow_token = response_json["flow_token"]
    if flow_token[len(flow_token) - 1] != "7":
        raise Exception(f"X_API_ERROR_MESSAGE: {response_json}")


def submit_password(
    sess,
    password: str,
):
    response = requests.post(
        url=SUBMIT_PASSWORD_REQUEST_COMPONENTS["url"],
        headers=SUBMIT_PASSWORD_REQUEST_COMPONENTS["headers"](
            sess.cookies, sess.x_guest_token
        ),
        json=SUBMIT_PASSWORD_REQUEST_COMPONENTS["payload"](sess.flow_token, password),
    )
    if response.status_code != 200:
        raise Exception(f"Error: {response.text}. Status code: {response.status_code}")

    response_json = response.json()
    flow_token = response_json["flow_token"]
    if flow_token[len(flow_token) - 2 :] != "13":
        raise Exception(f"X_API_ERROR_MESSAGE: {response_json}")

    cookies = response.headers["set-cookie"]
    cookies = cookie_to_dict(cookies)

    auth_token, ct0, user_id = (cookies["auth_token"], cookies["ct0"], cookies["twid"])
    user_id: str = user_id
    sess.cookies.dict["auth_token"] = auth_token
    sess.user_id = user_id.strip("u=")
    sess.cookies.dict["ct0"] = ct0
    sess.x_csrf_token = ct0
