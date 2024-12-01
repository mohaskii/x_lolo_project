from datetime import date as Date, datetime
from .user import User
from dataclasses import dataclass
from .media import Media
from typing import List
from .request_payload_and_headers import LIKE_POST_REQUEST_COMPONENT
import requests


@dataclass
class Post:
    """
    Represents a post (tweet) on the X (formerly Twitter) platform.

    This class encapsulates the data and functionality related to a single post.
    It includes attributes for various post properties and methods for interacting
    with the post.

    Attributes:
        id (str | None): The unique identifier of the post.
        owner_username (str | None): The username of the post's author.
        owner_user_id (str | None): The user ID of the post's author.
        linked_session: The session object associated with this post.
        creation_date (Date | None): The date the post was created.
        like_count (int | None): The number of likes on the post.
        text_content (str | None): The text content of the post.
        comment_count (int | None): The number of comments on the post.
        view (int | None): The number of views on the post.
        repost (int | None): The number of reposts on the post.

    Methods:
        __init__: Initializes a new Post object.
        load_by_creation_result: Loads post data from a creation result.
    """
    id: str | None = None
    user_owner: User = None
    creation_date: Date | None = None
    like_count: int | None = None
    text_content: str | None = None
    comment_count: int | None = None
    view: int | None = None
    repost: int | None = None
    medias: List[Media] | None = None

    def __init__(self, linked_session):
        """
            Initializes a new Post object..

            :param linked_session: The session object associated with this post.
            """
        self.linked_session = linked_session

    def load_by_creation_result(self, result):
        """
        Loads post data from a creation result.

        This method populates the Post object's attributes with data from a tweet creation result.
        It extracts information such as the post ID, creation date, content, and author details.

        :param result: The creation result data from the API.
        :raises Exception: If there's a potential change in the API structure.
        """
        try:
            # Extract the tweet result from the API response
            result = result["data"]["create_tweet"]["tweet_results"]["result"]

            # Set the post ID
            self.id = result["rest_id"]

            # Parse and set the creation date
            self.creation_date = datetime.strptime(
                result["legacy"]["created_at"], '%a %b %d %H:%M:%S %z %Y')

            # Initialize engagement metrics (likes, views, reposts, comments)
            self.like_count = 0
            self.view = 0
            self.repost = 0
            self.comment_count = 0

            # Set the owner's user ID from the linked session
            self.owner_user_id = self.linked_session.user_id

            # Set the post content
            self.text_content = result["legacy"]["full_text"]

            # Extract the user_data
            result = result["core"]["user_results"]
            new_user = User(linked_session=self.linked_session)
            new_user.load_by_json_result(result)
            self.user_owner = new_user

        except Exception:
            # Raise an exception if there's a potential change in the API structure
            raise Exception(
                "Potential change on the API. Hint: func:`load_by_creation_result`")

    def load_by_result_json(self, result):
        if "limitedActionResults" in result:
            result = result["tweet"]
        self.id = result["rest_id"]
        user_owner = User(linked_session=self.linked_session)
        user_owner.load_by_json_result(result["core"]["user_results"])
        self.user_owner = user_owner
        if result["views"].get("count"):
            self.view = int(result["views"]["count"])
        result = result["legacy"]
        self.like_count = result["favorite_count"]
        self.repost = result["retweet_count"]
        self.comment_count = result["reply_count"]
        self.creation_date = datetime.strptime(
            result["created_at"], '%a %b %d %H:%M:%S %z %Y'
        )
        self.text_content = result["full_text"]
        result = result["entities"]
        if result.get("media") is None:
            return
        result = result["media"]
        self.medias = []
        for entity in result:
            media = Media(self.linked_session)
            media.load_from_json(entity)
            self.medias.append(media)

    # Non-implemented methods (not included in the class comment)

    def like(self):
        response = requests.post(
            url=LIKE_POST_REQUEST_COMPONENT["url"],
            headers=LIKE_POST_REQUEST_COMPONENT["headers"](
                self.linked_session),
            json=LIKE_POST_REQUEST_COMPONENT["payload"](self.id)
        )
        if response.status_code != 200:
            raise Exception(
                f"Error: {response.text}. Status code: {response.status_code}")
        return

    def unlike(self):
        # TODO
        return

    def comment(self, content: str):
        # TODO
        return

    def share(self):
        # TODO
        return
