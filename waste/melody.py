import time

import click
import yt_dlp

from subprocess import PIPE, Popen

from waste import draw
from waste import gui
from waste import yt


WIDTH = 600
HEIGHT = 1200

TEXT_COLOR = draw.BLACK
BACKGROUND = draw.PALE_YELLOW


@click.command()
@click.option("--font-name", type=str)
def melody(font_name):
    font_name = font_name or "vt220-normal-10x20"
    Melody(font=font_name).run()


class Melody(gui.Window):
    def __init__(self, font):
        super().__init__(
            "Melody 🎵",
            width=WIDTH,
            height=HEIGHT,
            zoom=1,
            background=BACKGROUND,
        )

        self.font = self.font_manager.font(font)
        self.x_margin = self.font.w
        self.y_margin = self.font.h

        self.text_input = gui.TextView(
            self.x_margin,
            self.y_margin,
            self.w - (self.x_margin * 2),
            self.font.h + 4,
            TEXT_COLOR,
            BACKGROUND,
            self.font,
            x_pad=2,
            y_pad=2,
            border=gui.Border.BOTTOM
        )

        self.current_track_view = gui.TextView(
            self.x_margin,
            self.text_input.y + self.text_input.h + 4,
            self.w - (self.x_margin * 2),
            self.font.h + 4,
            TEXT_COLOR,
            BACKGROUND,
            self.font,
            x_pad=2,
            y_pad=2,
            border=gui.Border.ALL,
        )

        self.error_view = gui.TextView(
            0,
            self.h - self.font.h - 8,
            self.w,
            self.font.h + 8,
            TEXT_COLOR,
            BACKGROUND,
            self.font,
            x_pad=self.font.w,
            y_pad=4,
            border=gui.Border.TOP,
        )

        self.tracks_view = gui.TextView(
            self.x_margin,
            self.text_input.y + self.text_input.h + ((self.font.h + 4) * 2),
            self.w - (self.x_margin * 2),
            self.font.h * 50,
            TEXT_COLOR,
            BACKGROUND,
            self.font,
            x_pad = self.font.w,
            y_pad = 4,
            border=gui.Border.SIDES,
        )

        self.yt = yt.Searcher()
        self.process = None
        self.command_buffer = []
        self.tracks = []

        self.disable_resizing()
        self.move(0, 0)
        self.clear()

    def redraw(self):
        self.text_input.draw_on(self.screen)
        self.current_track_view.draw_on(self.screen)
        self.tracks_view.draw_on(self.screen)
        self.error_view.draw_on(self.screen)

    def on_text_input(self, txt):
        self.command_buffer.append(txt)
        self.text_input.draw("".join(self.command_buffer))

    def on_key_down(self, key):
        if key == gui.Modifier.BACKSPACE.name:
            if not self.command_buffer:
                return

            self.command_buffer.pop()
            self.text_input.draw("".join(self.command_buffer))

        if key == gui.Modifier.ENTER.name:
            expression = "".join(self.command_buffer)
            self.command_buffer = []
            self.text_input.clear()
            self.eval(expression)

        if key == gui.Modifier.ESC.name:
            self.quit()

    def eval(self, expression):
        fn, *rest = expression.split()
        arg = " ".join(rest)
        match fn:
            case "search":
                if not arg:
                    return

                self.tracks = self.yt.search(arg)
                self.tracks_view.draw(self.format_tracks())
            case "play":
                if not arg:
                    self.set_error("Missing track number!")
                    return

                index = int(arg) - 1
                media = self.tracks[index]

                url = (
                    yt_dlp
                    .YoutubeDL({"quiet": True, "format": "best"})
                    .extract_info(media.playback_url, download=False)
                    .get("url")
                )

                if not url:
                    self.set_error(f"Missing url for {media.title}!")
                    return

                if self.process:
                    self.process.terminate()

                self.process = Popen(
                    ["ffplay", "-i", url, "-autoexit", "-loglevel", "quiet"],
                    stdin=PIPE,
                    stdout=PIPE,
                    stderr=PIPE
                )

                self.current_track_view.draw(f"Current: {media.title}")
                self.focus()

            case "stop":
                if self.process:
                    self.process.terminate()
                    self.current_track_view.clear()
            case "quit":
                self.quit()
            case _:
                self.set_error(f"unrecognized {expression =}!")
                return
        self.error_view.clear()

    def set_error(self, message):
        self.error_view.draw(message)

    def format_tracks(self):
        def format_index(index):
            index = index + 1
            if index < 10:
                return f"{index: 2d}"
            return str(index)

        def format_track(index, track):
            return "\n".join([
                f"{format_index(index)} -- {track.title}",
                f"      {track.length}",
            ])

        return "\n".join(format_track(i, t) for i, t in enumerate(self.tracks))

    def quit(self):
        if self.process:
            self.process.terminate()
            self.current_track_view.clear()
        super().quit()
