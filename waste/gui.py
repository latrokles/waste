import ctypes
import pathlib
import sys

import click
import sdl2

from waste import draw

DEFAULT_ZOOM = 2
DEFAULT_FPS = 30
ENCODING = "utf-8"


class EventOpsMixin:
    def on_mouse_input(self, mousedev):
        pass

    def on_key_input(self, keyboarddev):
        pass

    def on_text_input(self, text):
        pass

    def on_file_drop(self, pathname):
        pass

    def on_clipboard_update(self, text):
        pass

    def copy_to_clipboard(self, text):
        sdl2.SDL_SetClipboardText(text.encode("utf-8"))


class GraphicOpsMixin:
    def redraw(self):
        pass

    def draw_path(self, points, brush, op=draw.Operation.STORE):
        pass

    def draw_line(self, x0, y0, x1, y2, brush, op=draw.Operation.STORE):
        pass

    def draw_rectangle(
        self, origin, corner, brush, op=draw.Operation.STORE, fill=False
    ):
        pass

    def draw_circle(
        self, centerx, centery, radius, brush, op=draw.Operation.STORE, fill=False
    ):
        pass

    def draw_image(self, x, y, image):
        # TODO implement in terms of bitblt on form
        src_col_start = 0
        src_col_end = image.w
        src_row_end = image.h

        if image.w > self.w:
            src_col_end = min(self.w + 1, image.w)

        if image.h > self.h:
            src_row_end = min(self.h + 1, image.h)

        dst_col_end = x + image.w
        dst_row_end = y + image.h

        if dst_col_end >= self.w:
            dst_col_end = dst_col_end - (dst_col_end - self.w)

        if dst_row_end >= self.h:
            dst_row_end = dst_row_end - (dst_row_end - self.h)

        for row in range(src_row_end):
            self.screen.put_row_bytes(
                src_col_start,
                row,
                image.row_bytes(0, row, src_col_end),
            )

    def draw_text(self, x, y, text, font, fg_color, bg_color):
        posx = x
        posy = y
        for char in text:
            if char == "\n":
                posx = x
                posy += font.h
                continue

            self.draw_glyph(
                posx, posy, font.glyph(char), font.w, font.h, fg_color, bg_color
            )
            posx += font.w

    def draw_glyph(self, x, y, glyph, w, h, fg_color, bg_color):
        for row in range(h):
            for col in range(w):
                is_set = (glyph[row] >> ((w - 1) - col)) & 0x1

                val = bg_color
                if is_set:
                    val = fg_color

                self.put_pixel(x + col, y + row, val)

    def put_pixel(self, x, y, color):
        out_of_bounds_in_x = (x < 0) or x >= self.w
        out_of_bounds_in_y = (y < 0) or y >= self.h

        if out_of_bounds_in_x or out_of_bounds_in_y:
            return

        self.screen.put_color_at(x, y, color)


class Window(EventOpsMixin, GraphicOpsMixin):
    def __init__(
        self,
        title,
        width,
        height,
        zoom=DEFAULT_ZOOM,
        fps=DEFAULT_FPS,
        background=None,
        window_opts=0,
    ):
        self.w = width
        self.h = height
        self.zoom = zoom
        self.fps = fps

        self.background = background or draw.BLACK
        self.screen = draw.Form(0, 0, self.w, self.h)  # TODO use factory method
        self.mousex = 0
        self.mousey = 0
        self.pmousex = 0
        self.pmousey = 0

        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) < 0:
            err = f"Cannot initialize SDL, err={sdl2.SDL_GetError()}"
            raise RuntimeError(err)

        title = f"{title} - ({self.w} x {self.h} : {self.zoom})"
        self.window = sdl2.SDL_CreateWindow(
            title.encode("utf-8"),
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            self.w * self.zoom,
            self.h * self.zoom,
            window_opts,
        )

        self.renderer = sdl2.render.SDL_CreateRenderer(
            self.window,
            -1,
            sdl2.SDL_RENDERER_PRESENTVSYNC,
        )

        self.texture = sdl2.SDL_CreateTexture(
            self.renderer,
            sdl2.SDL_PIXELFORMAT_RGBA8888,
            sdl2.SDL_TEXTUREACCESS_STREAMING,
            self.w,
            self.h,
        )

        sdl2.SDL_SetWindowMinimumSize(self.window, self.w, self.h)
        sdl2.render.SDL_RenderSetLogicalSize(self.renderer, self.w, self.h)
        sdl2.render.SDL_RenderSetIntegerScale(self.renderer, 1)
        sdl2.SDL_StartTextInput()

    @property
    def position(self):
        x, y = ctypes.c_int(0), ctypes.c_int(0)
        sdl2.SDL_GetWindowPosition(self.window, x, y)
        return int(x.value), int(y.value)

    @property
    def size(self):
        return (self.w, self.h)

    def move(self, x, y):
        sdl2.SDL_SetWindowPosition(self.window, x, y)

    def show(self):
        sdl2.SDL_ShowWindow(self.window)

    def hide(self):
        sdl2.SDL_HideWindow(self.window)

    def raisewin(self):
        sdl2.SDL_RaiseWindow(self.window)

    def minimize(self):
        sdl2.SDL_MinimizeWindow(self.window)

    def restore(self):
        sdl2.SDL_RestoreWindow(self.window)

    def display_borders(self):
        sdl2.SDL_SetWindowBordered(self.window, True)

    def hide_borders(self):
        sdl2.SDL_SetWindowBordered(self.window, False)

    def enable_resizing(self):
        sdl2.SDL_SetWindowResizable(self.window, True)

    def disable_resizing(self):
        sdl2.SDL_SetWindowResizable(self.window, False)

    def enable_always_on_top(self):
        sdl2.SDL_SetWindowAlwaysOnTop(self.window, True)

    def disable_always_on_top(self):
        sdl2.SDL_SetWindowAlwaysOnTop(self.window, False)

    def run(self):
        next_tick = 0
        while True:
            tick = sdl2.SDL_GetTicks()
            if tick < next_tick:
                sdl2.SDL_Delay(next_tick - tick)

            next_tick = tick + int(1_000 / self.fps)
            event = sdl2.SDL_Event()
            while sdl2.SDL_PollEvent(event):
                self.dispatch_event(event)
        self.quit()

    def dispatch_event(self, event):
        match event.type:
            case sdl2.SDL_QUIT:
                self.quit()
            case (
                sdl2.SDL_MOUSEMOTION | sdl2.SDL_MOUSEBUTTONUP | sdl2.SDL_MOUSEBUTTONDOWN
            ):
                self.handle_mouse(event)
            case sdl2.SDL_KEYDOWN:
                self.handle_key(event)
            case sdl2.SDL_TEXTINPUT:
                self.handle_text(event)
            case sdl2.SDL_DROPFILE:
                self.handle_drop(event)
            case sdl2.SDL_CLIPBOARDUPDATE:
                self.handle_clipboard_update(event)
            case sdl2.SDL_WINDOWEVENT:
                if event.window.event == sdl2.SDL_WINDOWEVENT_EXPOSED:
                    self.redisplay()
            case _:
                pass

    def handle_mouse(self, event):
        if event.type == sdl2.SDL_MOUSEMOTION:
            self.pmousex = self.mousex
            self.pmousey = self.mousey

            self.mousex = event.motion.x
            self.mousey = event.motion.y

        self.on_mouse_input(event)  # TODO pass a generic event (no SDL)
        self.redisplay()

    def handle_key(self, event):
        self.on_key_input(event.key.keysym.sym)  # TODO pass a generic event (no SDL)
        self.redisplay()

    def handle_text(self, event):
        self.on_text_input(event.text.text.decode("utf-8"))
        self.redisplay()

    def handle_drop(self, event):
        self.on_file_drop(pathlib.Path(event.drop.file.decode(ENCODING)))
        self.redisplay()

    def handle_clipboard_update(self, event):
        self.on_clipboard_update(sdl2.SDL_GetClipboardText().decode("utf-8"))
        self.redisplay()

    def clear(self):
        if self.background == draw.BLACK:
            self.screen.clear()
            return
        self.screen.fill(self.background)

    def redisplay(self):
        self.redraw()
        sdl2.SDL_UpdateTexture(
            self.texture, None, self.screen.bytes, self.screen.w * self.screen.depth
        )
        sdl2.SDL_RenderClear(self.renderer)
        sdl2.SDL_RenderCopy(self.renderer, self.texture, None, None)
        sdl2.SDL_RenderPresent(self.renderer)

    def quit(self):
        sdl2.SDL_StopTextInput()
        sdl2.SDL_DestroyTexture(self.texture)
        sdl2.SDL_DestroyRenderer(self.renderer)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()
        sys.exit(0)


@click.group()
def gui_test():
    pass


@gui_test.command()
def basic():
    from waste.font import UNICODE_8x15

    class BasicTest(Window):
        def __init__(self, font):
            super().__init__("basic window test", width=420, height=360)
            self.font = font

        def redraw(self):
            self.clear()
            x = self.mousex
            y = self.mousey
            self.draw_text(x, y, f"({x}, {y})", self.font, draw.WHITE, draw.BLACK)

    BasicTest(font=UNICODE_8x15).run()



@gui_test.command()
def textinput():
    from waste.font import UNICODE_8x15

    class TextInputTest(Window):
        def __init__(self, font):
            super().__init__("textinput test", width=420, height=360, background=draw.PALE_YELLOW)
            self.font = font
            self.doc = []

        def on_text_input(self, text):
            self.doc.append(text)

        def on_key_input(self, sym):
            if sym == sdl2.SDLK_RETURN:
                self.doc.append("\n")

        def redraw(self):
            text = "".join(self.doc)
            print(text)
            self.clear()
            self.draw_text(0, 0, text, self.font, draw.BLACK, draw.PALE_YELLOW)

    TextInputTest(font=UNICODE_8x15).run()


@gui_test.command()
@click.option("--size", type=(int, int))
@click.argument("image-location")
def image(image_location, size):
    w, h = None, None
    if size:
        w, h = size

    if image_location.startswith("http"):
        img = draw.ImageForm.from_url(image_location, width=w, height=h)
    else:
        img = draw.ImageForm.from_path(image_location, width=w, height=h)

    w = Window("image test", width=420, height=360)
    w.draw_image(0, 0, img)
    w.run()
