import code
import json
import os
import pprint
import readline
import requests
import socket
import time

from dataclasses import dataclass
from functools import cache
from typing import List
from subprocess import PIPE, Popen
from urllib.parse import urlencode


def main():
    Aidem().start()


CMD_HELP = """
Supported commands:
- /search
- /play-audio
- /play-video
- /pause
- /resume
- /stop
- /quit
- help
"""


class Aidem(code.InteractiveConsole):
    def __init__(self, *args):
        super().__init__(args)
        self.mpv = MPVProcess()
        self.yt = YTMediaFinder()
        self.results = []

    def runsource(self, source, filename="<input>", symbol="single"):
        if len(source) == 0:
            return

        cmd, *rest = source.split()
        arg = " ".join(rest)
        match cmd:
            case "/search":
                self.do_search(arg)
            case "/play-audio":
                self.do_play-audio(arg)
            case "/play-video":
                self.do_play_video(arg)
            case "/pause":
                self.do_pause()
            case "/resume":
                self.do_resume()
            case "/stop":
                self.do_stop()
            case "/quit":
                self.do_quit()
            case "/help":
                self.do_help()
            case _:
                print(f"unrecognized command={cmd}. try again...")

    def do_search(self, query):
        def format_index(index):
            index = index + 1
            if index < 10:
                return f"{index: 2d}"
            return str(index)

        self.results = self.yt.search(query)
        for i, r in enumerate(self.results):
            print(f"{format_index(i)} -- {r.title}\n      {r.playback_url}\n")

    def do_play_audio(self, index):
        index = int(index)
        r = self.results[index - 1]
        print(f"Playing Audio for {index}: {r.title}({r.playback_url})")
        self.mpv.send(["set_property", "video", "no"])
        self.mpv.send(["loadfile", r.playback_url])

    def do_play_video(self, index):
        index = int(index)
        r = self.results[index - 1]
        print(f"Playing Audio for {index}: {r.title}({r.playback_url})")
        self.mpv.send(["set_property", "video", "auto"])
        self.mpv.send(["loadfile", r.playback_url])

    def do_pause(self):
        self.mpv.send(["set_property", "pause", True])

    def do_resume(self):
        self.mpv.send(["set_property", "pause", False])

    def do_stop(self):
        print("Stopping...")
        self.mpv.send(["stop"])

    def do_quit(self):
        self.mpv.stop()

    def do_help(self):
        print(CMD_HELP)

    def start(self):
        self.mpv.start()
        self.interact(banner="Aidem - a distraction free player...", exitmsg="bye!")
        self.mpv.stop()


class MPVProcess:
    CMD = 'mpv --idle --input-ipc-server=/tmp/mpvsocket'
    SOCK = '/tmp/mpvsocket'

    def __init__(self):
        self.ipc = None
        self.process = None
        self.running = False

    def start(self):
        args = MPVProcess.CMD.split()
        self.process = Popen(args, start_new_session=True, shell=False)
        time.sleep(0.5)
        self.ipc = socket.socket(socket.AF_UNIX)
        self.ipc.connect(MPVProcess.SOCK)

    def stop(self):
        if self.process is None:
            return
        self.process.kill()

    def send(self, command):
        message = (
            json
            .dumps({"command": command})
            .encode("utf-8")
        )
        self.ipc.send(message + b'\n')


class YTMediaFinder:
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'

    @cache
    def search(self, query_text):
        key = urlencode({'key': os.getenv('YT_KEY')})
        url = f'https://www.youtube.com/youtubei/v1/search?{key}'
        body = self._build_request(query_text)
        response = requests.post(
            url,
            headers={'User-Agent': YTMediaFinder.USER_AGENT},
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
            YTMediaResult.from_rendered_video_item(video_item)
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
class YTMediaResult:
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
