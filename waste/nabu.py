import pathlib
import subprocess

import click

from waste.draw import Window, fetch_glyph
from waste.draw import BLACK, PALE_YELLOW

CELL_W = 9
CELL_H = 15
COLS = 50
ROWS = 50
PAD_X = 2
PAD_Y = 1
WIDTH = CELL_W * (COLS + (2 * PAD_X))
HEIGHT = CELL_H * (ROWS + (2 * PAD_Y))

TEXT_COLOR = BLACK
BACKGROUND = PALE_YELLOW


@click.command()
def nabu():
    Nabu()


class Nabu(Window):
    def __init__(self):
        self.state_to_message = {
            "WAITING": "Drop image file to transcribe here.",
            "PROCESSING": "Processing file.",
        }

        self.state = "WAITING"
        super().__init__(
            "NABU 📷 -> 📃",
            width=WIDTH,
            height=HEIGHT,
            zoom=1,
            is_resizable=False,
            has_border=False,
            background=BACKGROUND,
        )
        # TODO set window position to top left corner
        # TODO make window always in top (is this even possible)
        # TODO ensure script location
        # TODO parse configuration from homedir

    def redraw(self):
        # TODO refactor window code to make this more ergonomic
        self.clear()
        text = self.state_to_message.get(self.state)
        self.draw_text(2 * CELL_W, 1 * CELL_H, text)
        super().redraw()

    def handle_drop(self, event):
        # TODO make paths configurable
        # TODO set some state to display message, should I even swap messages?
        script_path = pathlib.Path.home() / "Desktop/OCR/ocr.swift"
        src_pathname = event.drop.file.decode("utf-8")
        extension = pathlib.Path(src_pathname).suffix
        dst_pathname = src_pathname.replace(extension, ".txt")

        ocr_cmd = ["swift", str(script_path), src_pathname]
        with subprocess.Popen(ocr_cmd, stdout=subprocess.PIPE) as ocr_proc:
            with open(dst_pathname, "w", encoding="utf-8") as output_file:
                for line in ocr_proc.stdout:
                    output_file.write(line.decode('utf-8'))

        launch_cmd = ["open", dst_pathname]
        subprocess.Popen(launch_cmd)

    def draw_text(self, x, y, text):
        posx = x
        posy = y
        for char in text:
            if char == "\n":
                posx = x
                posy += CELL_H
                continue

            self.draw_glyph(
                posx, posy, fetch_glyph(char), CELL_W, CELL_H, TEXT_COLOR, BACKGROUND
            )
            posx += CELL_W
