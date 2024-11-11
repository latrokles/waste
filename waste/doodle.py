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
        self.ui_pen = draw.Form(0, 0, 1, 1)
        self.ui_pen.fill(draw.BLACK)
        self.ui_updated = True

        self.canvas = draw.Form(0, 0, 470, 300)
        self.clear_canvas()
        self.canvas_updated = True

        self.pen = draw.Form(0, 0, 1, 1)
        self.pen.fill(draw.BLACK)

        self.clear()
        self.redraw()

    def redraw(self):
        self.draw_canvas()
        self.draw_ui()

    def draw_ui(self):
        if not self.ui_updated:
            return

        self.screen.draw_rectangle(
            draw.Point(5, self.h - 18),
            draw.Point(475, self.h - 5),
            self.ui_pen,
        )
        self.screen.draw_rectangle(
            draw.Point(5, 5),
            draw.Point(5 + self.canvas.w, 5 + self.canvas.h),
            self.ui_pen,
        )

    def draw_canvas(self):
        if self.mouse.lb:
            # TODO implement Point.translate
            p0 = draw.Point(self.mouse.prev_position.x - 5, self.mouse.prev_position.y - 5)
            p1 = draw.Point(self.mouse.position.x - 5, self.mouse.position.y - 5)
            self.canvas.draw_line(p0, p1, self.pen)
            self.canvas_updated = True

        if self.canvas_updated:
            self.screen.bitblt(self.canvas, self.canvas.rect.clone(), draw.Point(5, 5))
            self.canvas_updated = False

    def on_key_down(self, key):
        if key == "q":
            self.quit()
        if key == gui.Modifier.ESC.name:
            self.clear_canvas()

    def clear_canvas(self):
        self.canvas.fill(draw.WHITE)
        self.canvas_updated = True


if __name__ == "__main__":
    doodle()
