from typing import Dict, Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class User:
    """
    Represents a user on the X (formerly Twitter) platform.

    This class encapsulates the data and functionality related to a single user.
    It includes attributes for various user properties and methods for interacting
    with the user data.

    Attributes:
        id (str | None): The unique identifier of the user.
        rest_id (str | None): The REST API ID of the user.
        username (str | None): The username of the user.
        name (str | None): The full name of the user.
        profile_image_url (str | None): The URL of the user's profile image.
        bio (str | None): The user's bio or description.
        location (str | None): The user's location.
        website (str | None): The user's website.
        created_at (datetime | None): The date the user account was created.
        followers_count (int | None): The number of followers the user has.
        following_count (int | None): The number of users the user is following.
        tweet_count (int | None): The number of tweets the user has posted.
        is_verified (bool | None): Whether the user is verified.
    """

    id: Optional[str] = None
    rest_id: Optional[str] = None
    username: Optional[str] = None
    name: Optional[str] = None
    profile_image_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    created_at: Optional[datetime] = None
    followers_count: Optional[int] = None
    following_count: Optional[int] = None
    tweet_count: Optional[int] = None
    is_verified: Optional[bool] = None
    # is_private: Optional[bool] = None

    def load_by_json_result(self, result: Dict):
        """
        Loads user data from a JSON result.

        This method populates the User object's attributes with data from a user
        JSON result. It extracts information such as the user ID, username, name,
        profile image URL, bio, location, creation date, follower count, following
        count, tweet count, and verification status.

        :param result: The user JSON result data.
        :raises Exception: If there's a potential change in the API structure.
        """
        try:
            # Extract the user result from the API response
            user_data = result["result"]

            # Set the user ID
            
            self.id = user_data["rest_id"]

            # Set the username and name
            self.username = user_data["legacy"]["screen_name"]
            self.name = user_data["legacy"]["name"]

            # Set the profile image URL
            self.profile_image_url = user_data["legacy"]["profile_image_url_https"]

            # Set the bio
            self.bio = user_data["legacy"]["description"]

            # Set the location
            self.location = user_data["legacy"]["location"]

            # Parse and set the creation date
            self.created_at = datetime.strptime(
                user_data["legacy"]["created_at"], '%a %b %d %H:%M:%S %z %Y'
            )

            # Set follower and following counts
            self.followers_count = user_data["legacy"]["followers_count"]
            self.following_count = user_data["legacy"]["friends_count"]

            # Set tweet count
            self.tweet_count = user_data["legacy"]["statuses_count"]

            # Set verification status
            self.is_verified = user_data["legacy"]["verified"]

            # Set private account status
            # self.is_private = user_data["legacy"]["protected"]

        except Exception:
            # Raise an exception if there's a potential change in the API structure
            raise Exception(
                "Potential change on the API. Hint: func:`load_by_json_result`"
            )

    def __str__(self):
        return f"User @{self.username} (ID: {self.id}) - {self.name}"