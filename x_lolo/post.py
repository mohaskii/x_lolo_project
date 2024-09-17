from .session import Session
from datetime import date as Date


class Post:
    def __init__(self, linked_session: Session):
        self.id: int | None = None
        self.owner_username: str | None = None
        self.owner_user_id: int | None = None
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
