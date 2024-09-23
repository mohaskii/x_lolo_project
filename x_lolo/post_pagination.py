from .post import Post
from dataclasses import dataclass
from typing import List


@dataclass
class UserPostPaginator:
    """
    Represents pagination for retrieving posts.

    This class encapsulates the data and functionality related to post pagination.
    It includes attributes for various pagination properties and methods for interacting
    """
    posts_state: List[Post] | None = None
    next_token: str | None = None
    prev_token: str | None = None

    def __init__(self, linked_session, json_entries, username):
        self.linked_session = linked_session
        self.__load_from_json(json_entries)
        self.username = username

    def __load_from_json(self, json_entries):
        self.posts_state = []
        for v in json_entries:
            entry_id: str = v["entryId"]

            if entry_id.startswith("cursor-bottom"):
                self.next_token = v["content"]["value"]
                continue
            if entry_id.startswith("cursor-top"):
                self.prev_token = v["content"]["value"]
                continue
            if entry_id.startswith("tweet") == False:
                continue
            r = v["content"]["itemContent"]["tweet_results"]["result"]
            new_post = Post(self.linked_session)
            new_post.load_by_result_json(r)
            self.posts_state.append(new_post)
        return

    def next(self):
        """
        Fetches the next set of posts.

        If a next token is available, fetches the next set of posts.
        """
        data: List = self.linked_session.get_user_post_pagination_json(self.username, self.next_token)
        for v in data:
            if v["type"] == "TimelineAddEntries":
                data = v["entries"]
                break
        self.__load_from_json(data)
        return

    def previous(self):
        """
        Fetches the previous set of posts.

        If a previous token is available, fetches the previous set of posts.
        """
        data: List = self.linked_session.get_user_post_pagination_json(self.username, self.prev_token)
        for v in data:
            if v["type"] == "TimelineAddEntries":
                data = v["entries"]
                break
        self.__load_from_json(data)
        return
