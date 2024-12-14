import os

import requests

from dataclasses import dataclass
from functools import cache
from typing import List
from urllib.parse import urlencode

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'


class Searcher:
    @cache
    def search(self, query_text):
        key = urlencode({'key': os.getenv('YT_KEY')})
        url = f'https://www.youtube.com/youtubei/v1/search?{key}'
        body = self._build_request(query_text)
        response = requests.post(
            url,
            headers={'User-Agent': USER_AGENT},
            json=body,
            timeout=None,
            proxies={},
        )
        return self._parse_response(response.json())

    def _build_request(self, query_text):
        return {
            'context': {
                'client': {
                    'clientName': 'WEB',
                    'clientVersion': '2.20210224.06.00',
                    'newVisitorCookie': True,
                },
                'user': {
                    'lockedSafetyMode': False,
                }
            },
            'client': {
                'hl': 'en',
                'gl': 'US'
            },
            'query': query_text,
        }

    def _parse_response(self, json_response):
        contents = json_response.get('contents', {})

        section_list_contents = (
            contents
            .get('twoColumnSearchResultsRenderer', {})
            .get('primaryContents', {})
            .get('sectionListRenderer', {})
            .get('contents', [])
        )

        item_sections = [
            item_section
            for item_section
            in section_list_contents
            if 'itemSectionRenderer' in item_section.keys()
        ]

        item_section_contents = []
        for item in item_sections:
            item_section_contents.extend(
                item
                .get('itemSectionRenderer', {})
                .get('contents', [])
            )

        rendered_video_items = [
            section_item
            for section_item
            in item_section_contents
            if 'videoRenderer' in section_item.keys()
        ]

        return [
            VideoDetails.from_rendered_video_item(video_item)
            for video_item
            in rendered_video_items
        ]


@dataclass
class ThumbnailInfo:
    url: str
    width: int
    height: int

    @classmethod
    def from_dict(cls, thumb):
        return cls(
            url=thumb.get('url'),
            width=thumb.get('width'),
            height=thumb.get('height')
        )


@dataclass
class VideoDetails:
    uid: str
    title: str
    length: str
    thumbnails: List[ThumbnailInfo]

    @property
    def playback_url(self):
        return f'https://www.youtube.com/watch?v={self.uid}'

    @classmethod
    def from_rendered_video_item(cls, video_item):
        renderer = video_item.get('videoRenderer', {})
        video_id = renderer.get('videoId', None)
        title = renderer.get('title', {}).get('runs', [{}])[0].get('text', None)
        length = renderer.get('lengthText', {}).get('simpleText', None)
        thumbs = [
            ThumbnailInfo.from_dict(t)
            for t
            in renderer.get('thumbnail', {}).get('thumbnails', [{}])
        ]
        return cls(uid=video_id, title=title, length=length, thumbnails=thumbs)
