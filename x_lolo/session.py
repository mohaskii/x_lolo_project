from .utils import get_guest_ids as guest_ids
from .utils import auth_flows
from .cookie import Cookie
import yaml
from pathlib import Path
from typing import Dict, Any
from .request_payload_and_headers import TEXT_POST_REQUEST_COMPONENTS
import requests


class Session:
    def __init__(self, load_from: str | None = None):
        if load_from:
            self.__load_from_yaml(load_from)
            return
        self.cookies = guest_ids.get()
        self.x_guest_token = guest_ids.get_x_guest_token(self.cookies)
        self.x_csrf_token = ""
        return

    def login(self, username_email: str, password: str, save_session_to: str = None):
        flow_token, att_cookie = auth_flows.get(
            self.cookies, self.x_guest_token)
        self.flow_token = flow_token
        self.cookies.dict["att"] = att_cookie
        self.user_id = ""

        auth_flows.pass_next_link(self)
        auth_flows.submit_username(self, username_email)
        auth_flows.submit_password(self, password)

        if save_session_to:
            self.__save_to_yaml(self, save_session_to)

    def __save_to_yaml(cls, session: 'Session', filename: str = "session_data.yaml") -> None:
        data: Dict[str, Any] = {
            "cookies": session.cookies.dict,
            "x_guest_token": session.x_guest_token,
            "flow_token": session.flow_token,
            "x_csrf_token": session.x_csrf_token,
            "user_id": session.user_id 
        }

        file_path = Path(filename)
        with file_path.open("w") as f:
            yaml.dump(data, f, default_flow_style=False)

        print(f"Session data saved to {file_path}")

    def __load_from_yaml(self, filename: str = "session_data.yaml") -> 'Session':
        file_path = Path(filename)
        if not file_path.exists():
            raise FileNotFoundError(f"File {filename} not found")

        with file_path.open("r") as f:
            data = yaml.safe_load(f)

        self.cookies = Cookie(data["cookies"])
        self.x_guest_token = data["x_guest_token"]
        self.flow_token = data["flow_token"]
        self.x_csrf_token = data["x_csrf_token"]
        self.user_id = data["user_id"]

        return self

    def post_text(self, text):
        response = requests.post(
            url=TEXT_POST_REQUEST_COMPONENTS["url"], headers=TEXT_POST_REQUEST_COMPONENTS["headers"](self), json=TEXT_POST_REQUEST_COMPONENTS["payload"](text))
        if response.status_code!= 200:
            raise Exception(
                f"Error: {response.text}. Status code: {response.status_code}")
        response = response.json()
        if "errors" in response:
            raise Exception(f"X_API_ERROR_MESSAGE: {response['errors']}")