import click


from waste import draw
from waste import gui


@click.command()
def doodle():
    Doodle().run()


class Doodle(gui.Window):
    def __init__(self):
        super().__init__(
            "doodle - ✏️",
            width=480,
            height=360,
            zoom=2,
            background=draw.WHITE,
        )
        self.pen = draw.Form(0, 0, 1, 1)
        self.pen.fill(draw.BLACK)
        self.clear()

    def redraw(self):
        self.draw_line(self.mouse.px, self.mouse.py, self.mouse.x, self.mouse.y, self.pen)


if  __name__ == "__main__":
    doodle()