import click


from waste import draw
from waste import gui


@click.command()
def doodle():
    Doodle().run()


PALETTE = [
    draw.BLACK,
    draw.DARK_YELLOW,
    draw.PALE_BLUEGREEN,
    draw.PALE_GREYGREEN,
    draw.PALE_YELLOW,
    draw.PURPLE_BLUE,
    draw.YELLOW_GREEN,
    draw.WHITE,
]


class Doodle(gui.Window):
    def __init__(self):
        super().__init__(
            "doodle - ✏️",
            width=480,
            height=360,
            zoom=2,
            background=draw.PALE_YELLOW,
        )
        self.canvas = draw.Form(0, 0, 470, 300)
        self.pen = draw.Form(0, 0, 10, 10)
        self.pen.fill(draw.BLACK)
        self.clear_canvas()
        self.redraw()

    def redraw(self):
        self.draw_ui()
        self.draw_canvas()

    def draw_ui(self):
        self.clear()
        pass

    def draw_canvas(self):
        if self.mouse.lb:
            self.canvas.draw_line(
                self.mouse.prev_position, self.mouse.position, self.pen
            )
        self.screen.bitblt(self.canvas, self.canvas.rect.clone(), draw.Point(5, 5))

    def on_key_down(self, key):
        if key == "q":
            self.quit()
        if key == gui.Modifier.ESC.name:
            self.clear_canvas()

    def clear_canvas(self):
        self.canvas.fill(draw.WHITE)


if __name__ == "__main__":
    doodle()
