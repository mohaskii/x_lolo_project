from dataclasses import dataclass


@dataclass
class Media:
    id: int | None = None
    linked_session = None
    type: str | None = None
    image_url: str | None = None
    video_definitions_url: dict | None = None

    def __init__(self, linked_session):
        self.linked_session = linked_session

    def download_media(self, save_to_path: str) -> None:
        # TODO
        return

    def load_from_json(self, json_dict) -> None:
        self.type = json_dict["type"]
        self.id = json_dict["id_str"]
        if self.type == "photo":
            self.image_url = json_dict["media_url_https"]
            return
        if self.type == "video":
            self.video_definitions_url = json_dict["video_info"]["variants"]
            return
