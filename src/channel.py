import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется по id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id
        self.channel: dict = self.get_service().channels().list(id=self.__channel_id,
                                                                part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["localized"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count = int(self.channel["items"][0]["statistics"]["subscriberCount"])
        self.video_count = int(self.channel["items"][0]["statistics"]["videoCount"])
        self.view_count = int(self.channel["items"][0]["statistics"]["viewCount"])

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count + other.subscriber_count
        return ValueError

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count - other.subscriber_count
        return ValueError

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count < other.subscriber_count
        return ValueError

    def __le__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count <= other.subscriber_count
        return ValueError

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count > other.subscriber_count
        return ValueError

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count >= other.subscriber_count
        return ValueError

    def __eq__(self,other):
        if isinstance(other, self.__class__):
            return self.subscriber_count == other.subscriber_count
        return ValueError

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """
        Cоздает специальный объект для работы с API
        """
        return build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, file_name) -> None:
        info_dict = {"channel_id": self.__channel_id, "title": self.title, "description": self.description,
                     "url": self.url,
                     "subscriber_count": self.subscriber_count, "video_count": self.video_count,
                     "view_count": self.view_count}
        with open(file_name, "w") as f:
            json.dump(info_dict, f)
