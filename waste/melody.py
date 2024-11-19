import click

from waste import draw
from waste import gui


CELL_W = 9
CELL_H = 15
COLS = 50
ROWS = 50
PAD_X = 2
PAD_Y = 1
WIDTH = CELL_W * (COLS + (2 * PAD_X))
HEIGHT = CELL_H * (ROWS + (2 * PAD_Y))

TEXT_COLOR = draw.BLACK
BACKGROUND = draw.PALE_YELLOW


@click.command()
def melody():
    Melody(font="unicode_p9-8x15").run()


class Melody(gui.Window):
    def __init__(self, font):
        super().__init__(
            "Melody 🎵",
            width=WIDTH,
            height=HEIGHT,
            zoom=1,
            background=BACKGROUND,
        )
        self.font = font
        self.hide_borders()
        self.disable_resizing()
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

    def drawui(self):
        self.drawtrack(self.current_track)
        self.drawinput()
        self.drawresults()

    def drawtrack(self, track):
        self.draw_text(2 * CELL_W, 2 * CELL_H, "Track:", self.font, TEXT_COLOR, BACKGROUND)
        self.draw_text(2 * CELL_W, 3 * CELL_H, track, self.font, TEXT_COLOR, BACKGROUND)

    def drawinput(self):
        pass

    def drawresults(self):
        pass
