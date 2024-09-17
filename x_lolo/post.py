# from .session import Session
from datetime import date as Date, datetime


class Post:
    def __init__(self, linked_session):
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

    def load_by_creation_result(self, result):
        try:
            result = result["data"]["create_tweet"]["tweet_results"]["result"]
            self.id = result["rest_id"]
            self.creation_date = datetime.strptime(
                result["legacy"]["created_at"], '%a %b %d %H:%M:%S %z %Y')
            self.like = 0
            self.view = 0
            self.repost = 0
            self.comment_count = 0
            self.owner_user_id= self.linked_session.user_id 
            self.text_content = result["legacy"]["full_text"]
            result = result ["core"]["user_results"]["result"]
            self.owner_username  = result["legacy"]["screen_name"]
        except Exception :
            raise Exception("Error func : load_by_creation_result ")
        
