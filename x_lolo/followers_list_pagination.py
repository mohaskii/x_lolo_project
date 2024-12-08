from .user import User
from dataclasses import dataclass
from typing import List


@dataclass
class FollowerPaginator:
    """
    Represents pagination for retrieving followers.

    This class encapsulates the data and functionality related to follower pagination.
    It includes attributes for various pagination properties and methods for interacting
    """

    followers: List[User] | None = None
    next_token: str | None = None
    prev_token: str | None = None

    def __init__(self, linked_session, json_entries, username):
        self.linked_session = linked_session
        self.__load_from_json(json_entries)
        self.username = username

    def __load_from_json(self, json_entries):
        self.followers = []
        for v in json_entries:
            entry_id: str = v["entryId"]

            if entry_id.startswith("cursor-bottom"):
                self.next_token = v["content"]["value"]
                continue
            if entry_id.startswith("cursor-top"):
                self.prev_token = v["content"]["value"]
                continue
            if entry_id.startswith("user") == False:
                continue
            r = v["content"]["itemContent"]["user_results"]
            new_user  = User(self.linked_session)
            new_user.load_by_json_result(r)
            self.followers.append(new_user)
        return

    def next(self):
        """
        Fetches the next set of posts.

        If a next token is available, fetches the next set of posts.
        """
        data: List = self.linked_session.get_user_follower_pagination_json(
            self.username, self.next_token
        )
        for v in data:
            if v["type"] == "TimelineAddEntries":
                data = v["entries"]
                break
        self.__load_from_json(data)
        return

