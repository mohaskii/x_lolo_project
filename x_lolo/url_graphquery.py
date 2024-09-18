import urllib.parse
import json


class UrlGraphQuery:
    def __init__(self, url: str | None = None, query: dict | None = None):
        self.url = url
        self.query: dict = query

    def encode(self) -> str:
        encoded_result = {}
        for key, value in self.query.items():
            json_value = json.dumps(value)
            encoded_value = urllib.parse.quote(json_value)
            encoded_result[key] = encoded_value
        return self.url+"&".join([f"{key}={value}" for key, value in encoded_result.items()])

    def load(self, raw_query: str):
        raw_query_split = raw_query.split("?")
        self.url = raw_query_split[0]
        query_parts = raw_query_split[1].split("&")
        query_dict = {}
        for part in query_parts:
            key, value = part.split("=")
            decoded_value = urllib.parse.unquote(value)
            query_dict[key] = json.loads(decoded_value)
        self.query = query_dict
        return self
    def query_json(self):
        return json.dumps(self.query)
