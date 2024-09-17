from .utils import get_guest_ids as guest_ids
from .utils import auth_flows
from .cookie import Cookie
import yaml
from pathlib import Path
from typing import Dict, Any
from .request_payload_and_headers import TEXT_POST_REQUEST_COMPONENTS
import requests
from .post import Post

class Session:
    """
    Represents a user session for interacting with the X (formerly Twitter) API.
    
    This class manages the state and operations necessary for authenticating and 
    performing actions on behalf of a user.
    """
    
    def __init__(self, load_from: str | None = None):
        """
        Initializes a new session.
        
        If load_from is specified, loads session data from a YAML file.
        Otherwise, initializes a new session with cookies and a guest token.
        """
        if load_from:
            self.__load_from_yaml(load_from)
            return
        self.cookies = guest_ids.get()
        self.x_guest_token = guest_ids.get_x_guest_token(self.cookies)
        self.x_csrf_token = ""
        return

    def login(self, username_email: str, password: str, save_session_to: str = None):
        """
        Performs the login process.
        
        :param username_email: The email or username
        :param password: The password
        :param save_session_to: Path to save the session to (optional)
        """
        flow_token, att_cookie = auth_flows.get(self.cookies, self.x_guest_token)
        self.flow_token = flow_token
        self.cookies.dict["att"] = att_cookie
        self.user_id = ""
        
        # Performs the necessary steps for login
        auth_flows.pass_next_link(self)
        auth_flows.submit_username(self, username_email)
        auth_flows.submit_password(self, password)
        
        # Saves the session if requested
        if save_session_to:
            self.__save_to_yaml(self, save_session_to)

    def __save_to_yaml(cls, session: 'Session', filename: str = "session_data.yaml") -> None:
        """
        Saves the session data to a YAML file.
        
        :param session: The session object to save
        :param filename: The path to save the YAML file (default: "session_data.yaml")
        """
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
        """
        Loads session data from a YAML file.
        
        :param filename: The path to the YAML file (default: "session_data.yaml")
        :return: The loaded Session object
        """
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

    def add_post(self, text: str, media_url: str | None = None) -> Post:
        """
        Adds a new post (tweet) to the session.
        
        :param text: The text content of the post
        :param media_url: URL of the media to attach (optional)
        :return: The created Post object
        """
        # TODO: handle media upload
        response = requests.post(
            url=TEXT_POST_REQUEST_COMPONENTS["url"], 
            headers=TEXT_POST_REQUEST_COMPONENTS["headers"](self), 
            json=TEXT_POST_REQUEST_COMPONENTS["payload"](text)
        )
        if response.status_code != 200:
            raise Exception(f"Error: {response.text}. Status code: {response.status_code}")
        response_json = response.json()
        if "errors" in response_json:
            print(f"X_API_ERROR_MESSAGE: {response_json['errors']}")
            return None
        
        new_post = Post(self)
        new_post.load_by_creation_result(response_json)
        return new_post