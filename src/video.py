import os

from googleapiclient.discovery import build


class Video:
    """Класс для видео"""
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=video_id
                                                          ).execute()
        self.video_link = f"https://youtu.be/{self.video_id}"
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f"{self.video_title}"

    @classmethod
    def get_service(cls):
        """
        Cоздает специальный объект для работы с API
        """
        return build('youtube', 'v3', developerKey=cls.api_key)


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
