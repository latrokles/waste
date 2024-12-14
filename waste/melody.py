import click

from waste import draw
from waste import gui
from waste import yt


WIDTH = 500
HEIGHT = 1000

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
        self.ui_painter = draw.Form(0, 0, 1, 1)
        self.disable_resizing()
        self.move(0, 0)

        self.x_margin = self.font.w
        self.y_margin = self.font.h
        self.command_buffer = []
        self.error_message = ""
        self.tracks = []
        self.current_track_index = None
        self.ui_updated = True

        self.yt = yt.Searcher()

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
        self.drawerror()
        self.drawresults()
        self.ui_updated = False

    def drawtrack(self, track):
        return

        self.draw_text(2 * self.font.w, 2 * self.font.h, "Track:", self.font.name, TEXT_COLOR, BACKGROUND)
        self.draw_text(2 * self.font.h, 3 * self.font.h, track, self.font.name, TEXT_COLOR, BACKGROUND)

    def drawinput(self):
        self.screen.draw_rectangle(
            draw.Point(self.x_margin, self.y_margin),
            draw.Point(self.w - self.x_margin, self.y_margin + self.font.h + 4),
            self.ui_painter
        )
        self.draw_text(
            self.x_margin + 4,
            self.y_margin + 3,
            "".join(self.command_buffer),
            self.font.name,
            TEXT_COLOR,
            BACKGROUND,
        )

    def drawerror(self):
        self.screen.draw_line(
            draw.Point(0, self.h - (self.y_margin + self.font.h + 4)),
            draw.Point(self.w, self.h - (self.y_margin + self.font.h + 4)),
            self.ui_painter,
        )
        if self.error_message:
            self.draw_text(
                self.x_margin,
                self.h - (self.y_margin + self.font.h + 2),
                self.error_message,
                self.font.name,
                TEXT_COLOR,
                BACKGROUND
            )

    def drawresults(self):
        def format_index(index):
            index = index + 1
            if index < 10:
                return f"{index: 2d}"
            return str(index)

        results_x = self.x_margin + 4
        results_y = self.y_margin + self.y_margin + self.font.h + 4
        self.draw_text(results_x, results_y, "results:", self.font.name, TEXT_COLOR, BACKGROUND)

        results_y += self.font.h
        for i, r in enumerate(self.tracks):
            text = f"{format_index(i)} -- {r.title}\n{r.length}"
            _, results_y = self.draw_text(
                results_x,
                results_y,
                text,
                self.font.name,
                TEXT_COLOR,
                BACKGROUND,
            )
            results_y += 3


    def on_text_input(self, txt):
        self.command_buffer.append(txt)
        self.ui_updated = True

    def on_key_down(self, key):
        if key == gui.Modifier.BACKSPACE.name:
            if not self.command_buffer:
                return

            self.command_buffer.pop()

        if key == gui.Modifier.ENTER.name:
            expression = "".join(self.command_buffer)
            self.command_buffer = []
            self.error_message = ""
            self.eval(expression)

        if key == gui.Modifier.ESC.name:
            self.quit()

        self.ui_updated = True

    def eval(self, expression):
        fn, *args = expression.split()
        match fn:
            case "search":
                query = " ".join(args)
                self.tracks = self.yt.search(query)
                self.ui_updated = True
            case "play":
                pass
            case "quit":
                self.quit()
            case _:
                self.error_message = f"unrecognized {expression =}!"
