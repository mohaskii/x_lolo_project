from datetime import date as Date, datetime


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
        like (int | None): The number of likes on the post.
        text_content (str | None): The text content of the post.
        comment_count (int | None): The number of comments on the post.
        view (int | None): The number of views on the post.
        repost (int | None): The number of reposts on the post.

    Methods:
        __init__: Initializes a new Post object.
        load_by_creation_result: Loads post data from a creation result.
    """

    def __init__(self, linked_session):
        """
            Initializes a new Post object.

            This method sets up a new Post instance with default values for all attributes.
            It also stores a reference to the linked session object.

            :param linked_session: The session object associated with this post.
            """
        self.id: str | None = None
        self.owner_username: str | None = None
        self.owner_user_id: str | None = None
        self.linked_session = linked_session
        self.creation_date: Date | None = None
        self.like: int | None = None
        self.text_content: str | None = None
        self.comment_count: int | None = None
        self.view: int | None = None
        self.repost: int | None = None

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
            self.like = 0
            self.view = 0
            self.repost = 0
            self.comment_count = 0

            # Set the owner's user ID from the linked session
            self.owner_user_id = self.linked_session.user_id

            # Set the post content
            self.text_content = result["legacy"]["full_text"]

            # Extract the author's username
            result = result["core"]["user_results"]["result"]
            self.owner_username = result["legacy"]["screen_name"]
        except Exception:
            # Raise an exception if there's a potential change in the API structure
            raise Exception(
                "Potential change on the API. Hint: func:`load_by_creation_result`")

    # Non-implemented methods (not included in the class comment)
    def like(self):
        # TODO
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
