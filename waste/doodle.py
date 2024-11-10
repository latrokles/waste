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
        if self.mouse.lb:
            self.draw_line(self.mouse.prev_position, self.mouse.position, self.pen)

    def on_key_down(self, key):
        if key == "q":
            self.quit()
        if key == gui.Modifier.ESC.name:
            self.clear()


if __name__ == "__main__":
    doodle()
