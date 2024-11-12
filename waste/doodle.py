import click


from waste import draw
from waste import gui
from waste.font import UNICODE_8x15


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


WIDTH = 800
HEIGHT = 600
ZOOM = 1
MARGIN = 5
BORDER_SIZE = 1

@click.command()
def doodle():
    Doodle().run()


class Doodle(gui.Window):
    def __init__(self):
        super().__init__(
            "✏️ - doodle",
            width=WIDTH,
            height=HEIGHT,
            zoom=ZOOM,
            background=draw.PALE_YELLOW,
        )

        self.ui_pen = draw.Form(0, 0, BORDER_SIZE, BORDER_SIZE)
        self.ui_pen.fill(draw.BLACK)
        self.ui_updated = True

        self.command_buffer = []

        self.canvas = draw.Form(0, 0, self.w - (MARGIN * 2), int(self.h * 0.75))
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

        self.clear()

        # draw canvas
        self.screen.bitblt(
            self.canvas,
            self.canvas.rect.clone(),
            draw.Point(MARGIN, MARGIN),
        )

        # draw canvas frame
        self.screen.draw_rectangle(
            draw.Point(MARGIN - 1, MARGIN - 1),
            draw.Point(MARGIN + self.canvas.w,  MARGIN + self.canvas.h),
            self.ui_pen,
        )

        # draw command buffer
        self.screen.draw_rectangle(
            draw.Point(MARGIN, self.h - (MARGIN + 15 + 4)),
            draw.Point(self.w - MARGIN, self.h - MARGIN),
            self.ui_pen,
        )
        self.draw_text(
            7,
            self.h - 22,
            "".join(self.command_buffer),
            UNICODE_8x15,
            draw.BLACK,
            draw.PALE_YELLOW,
        )
        self.ui_updated = False

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

    def on_text_input(self, text):
        self.command_buffer.append(text)
        self.ui_updated = True

    def on_key_down(self, key):
        if key == gui.Modifier.BACKSPACE.name:
            if not self.command_buffer:
                return

            self.command_buffer.pop()
            self.ui_updated = True

        if key == gui.Modifier.ENTER.name:
            print("".join(self.command_buffer))
            self.command_buffer = []
            self.ui_updated = True

        if key == gui.Modifier.ESC.name:
            self.command_buffer = []
            self.ui_updated = True

    def clear_canvas(self):
        self.canvas.fill(draw.WHITE)
        self.canvas_updated = True


if __name__ == "__main__":
    doodle()
