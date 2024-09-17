from ..request_payload_and_headers import TEXT_POST_REQUEST_COMPONENTS


def post_text(session, text: str) -> None:
    response = requests.post(
        url=TEXT_POST_REQUEST_COMPONENTS["url"], headers=TEXT_POST_REQUEST_COMPONENTS["headers"](sess), json=TEXT_POST_REQUEST_COMPONENTS["payload"](sess.flow_token))