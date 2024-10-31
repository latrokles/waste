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
def melody():
    Melody().run()


class Melody(Window):
    def __init__(self):
        super().__init__(
            "Melody 🎵",
            width=WIDTH,
            height=HEIGHT,
            zoom=1,
            is_resizable=False,
            background=PALE_YELLOW,
            start_on_create=False,
        )
        self.clear()
        self.tracks = []
        self.current_track_index = None

    @property
    def current_track(self):
        if len(self.tracks) == 0:
            return "There are no tracks loaded."

        if self.current_track_index is None:
            return "No track selected."

        return self.tracks[self.current_track_index]

    def redraw(self):
        self.clear()
        self.drawui()
        super().redraw()

    def drawui(self):
        self.drawtrack(self.current_track)
        self.drawinput()
        self.drawresults()

    def drawtrack(self, track):
        self.draw_text(2 * CELL_W, 2 * CELL_H, "Track:")
        self.draw_text(2 * CELL_W, 3 * CELL_H, track)

    def drawinput(self):
        pass

    def drawresults(self):
        pass

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
