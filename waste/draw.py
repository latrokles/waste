import ctypes
import sys

import click
import requests
import sdl2

from dataclasses import dataclass

from PIL import Image
from waste.unicode8x15 import fetch_glyph
from waste.debug import debugmethod


class OutOfBoundsError(Exception):
    """Raised when trying to access a location outside a form."""


@dataclass
class Color:
    r: int
    g: int
    b: int
    a: int = 255

    @property
    def values(self):
        return [self.a, self.b, self.g, self.r]

    @classmethod
    def from_values(cls, values):
        alpha, blue, green, red = values
        return cls(red, green, blue, alpha)

    @staticmethod
    def from_int(rgbint):
        red = (rgbint & 0xFF0000) >> 16
        green = (rgbint & 0xFF00) >> 8
        blue = rgbint & 0xFF
        return Color(red, green, blue)

    @staticmethod
    def from_hexstr(hexstr):
        rgbint = int(hexstr, 16)
        return Color.from_int(rgbint)


BLACK = Color.from_int(0x000000)
DARK_YELLOW = Color.from_int(0xEEEE9E)
PALE_BLUEGREEN = Color.from_int(0xAAFFFF)
PALE_GREYGREEN = Color.from_int(0x9EEEEE)
PALE_YELLOW = Color.from_int(0xFFFFAA)  # from plan9port (didn't match)
PALE_YELLOW = Color.from_int(0xFFF5E1)  # from bitters/grid
PURPLE_BLUE = Color.from_int(0x8888CCF)
YELLOW_GREEN = Color.from_int(0x99994C)
WHITE = Color.from_int(0xFFFFFF)


@dataclass
class Point:
    x: int
    y: int

    def __str__(self):
        return f"P({self.x}, {self.y})"


@dataclass
class Rectangle:
    origin: Point
    corner: Point


class Form:
    def __init__(self, x, y, w, h, bitmap=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = Rectangle(Point(x, y), Point(x + w, y + h))

        if bitmap is None:
            bitmap = bytearray(self.w * self.h * self.depth * [0x00])
        self.bitmap = bitmap

    @property
    def depth(self):
        return 4

    @property
    def bytes(self):
        return (ctypes.c_char * len(self.bitmap)).from_buffer(self.bitmap)

    def color_at(self, x, y):
        _0th, _nth = self._pixel_bytes_range_at_point(x, y)
        pixel_bytes = self.bitmap[_0th:_nth]
        return Color.from_values(pixel_bytes)

    def put_color_at(self, x, y, color):
        _0th, _nth = self._pixel_bytes_range_at_point(x, y)
        self.bitmap[_0th:_nth] = color.values

    def row_bytes(self, x, y, pixel_count):
        if x + (pixel_count - 1) >= self.w:
            raise OutOfBoundsError(
                f"reading beyond bitmap width. start={x}, pixels={pixel_count}, bitmap width={self.w}"
            )

        byte_0 = (y * (self.w * self.depth)) + (x * self.depth)
        byte_n = byte_0 + (self.depth * (pixel_count - 1))
        return self.bitmap[byte_0:byte_n]

    def put_row_bytes(self, x, y, row_bytes):
        if x + ((len(row_bytes) - 1) / self.depth) >= self.w:
            raise OutOfBoundsError(
                f"writing beyond bitmap width. start={x}, pixel_count={len(row_bytes) / self.depth}"
            )

        byte_0 = (y * (self.w * self.depth)) + (x * self.depth)
        byte_n = byte_0 + len(row_bytes)
        self.bitmap[byte_0:byte_n] = row_bytes

    def fill(self, color):
        self.bitmap = bytearray(self.w * self.h * color.values)

    def clear(self):
        self.bitmap = bytearray(self.w * self.h * self.depth * [0x00])

    def _pixel_bytes_range_at_point(self, x, y):
        x_out_of_bounds = x < 0 or self.w <= x
        y_out_of_bounds = y < 0 or self.h <= y
        if x_out_of_bounds or y_out_of_bounds:
            raise OutOfBoundsError(f"({x=}, {y=}) is out of bounds of {self.rect}")

        byte_0 = (y * (self.w * self.depth)) + (x * self.depth)
        byte_n = byte_0 + self.depth
        return byte_0, byte_n


class ImageForm(Form):
    @classmethod
    def from_image(cls, img, width=None, height=None):
        if (width is not None) and (height is not None):
            img = img.resize((width, height))

        w = img.width
        h = img.height
        pixels = img.load()

        form = cls(0, 0, w, h)
        for y in range(h):
            for x in range(w):
                pixel_value = pixels[x, y]
                a = 255

                if len(pixel_value) == 4:
                    r, g, b, a = pixel_value
                else:
                    r, g, b = pixel_value
                values = [a, b, g, r]
                form.put_row_bytes(x, y, values)
        return form

    @classmethod
    def from_url(cls, url, width=None, height=None):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with Image.open(response.raw) as img:
            return cls.from_image(img, width, height)

    @classmethod
    def from_path(cls, pathname, width=None, height=None):
        with Image.open(pathname) as img:
            return cls.from_image(img, width, height)


DEFAULT_WIDHT = 64 * 8
DEFAULT_HEIGHT = 32 * 8
DEFAULT_ZOOM = 2
DEFAULT_FPS = 30


class MinimumWindow:
    pass


class GraphicsWindowMixin:
    pass


class TextWindowMixin:
    pass


class Window:
    def __init__(
        self,
        title,
        width=DEFAULT_WIDHT,
        height=DEFAULT_HEIGHT,
        zoom=DEFAULT_ZOOM,
        fps=DEFAULT_FPS,
        is_resizable=True,
        has_border=True,
        background=None,
        start_on_create=True,
    ):

        self.w = width
        self.h = height
        self.zoom = zoom
        self.fps = fps

        if background is None:
            background = BLACK
        self.background = background

        self.pixels = Form(0, 0, self.w, self.h)

        window_opts = 0
        if is_resizable:
            window_opts |= sdl2.SDL_WINDOW_RESIZABLE

        if not has_border:
            window_opts |= sdl2.SDL_WINDOW_BORDERLESS

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
        if start_on_create:
            self.run()

    @property
    def size(self):
        return (self.w, self.h)

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
                    self.redraw()
            case _:
                pass

    def handle_mouse(self, event):
        print("handling mouse event")
        self.redraw()

    def handle_key(self, event):
        print("handling key event")
        self.redraw()

    def handle_text(self, event):
        print("handling text event")
        self.redraw()

    def handle_drop(self, event):
        print("handling drop event")
        print(event.drop.file)
        self.redraw()

    def handle_clipboard_update(self, event):
        print("handling clipboard update")

    def clear(self):
        if self.background == BLACK:
            self.pixels.clear()
            return
        self.pixels.fill(self.background)

    def redraw(self):
        sdl2.SDL_UpdateTexture(
            self.texture, None, self.pixels.bytes, self.pixels.w * self.pixels.depth
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

    @debugmethod
    def draw_glyph(self, x, y, glyph, w, h, fg_color, bg_color):
        for row in range(h):
            for col in range(w):
                is_set = (glyph[row] >> ((w - 1) - col)) & 0x1

                val = bg_color
                if is_set:
                    val = fg_color

                self.put_pixel(x + col, y + row, val)

    @debugmethod
    def draw_image(self, x, y, image):
        src_col_start = 0
        src_col_end = image.w
        src_row_start = 0
        src_row_end = image.h

        if image.w > self.w:
            src_col_end = min(self.w + 1, image.w)

        if image.h > self.h:
            src_row_end = min(self.h + 1, image.h)

        dst_col_start = x
        dst_col_end = x + image.w
        dst_row_start = y
        dst_row_end = y + image.h

        if dst_col_end >= self.w:
            dst_col_end = dst_col_end - (dst_col_end - self.w)

        if dst_row_end >= self.h:
            dst_row_end = dst_row_end - (dst_row_end - self.h)

        for row in range(src_row_end):
            self.pixels.put_row_bytes(
                src_col_start,
                row,
                image.row_bytes(0, row, src_col_end),
            )

    @debugmethod
    def put_pixel(self, x, y, color):
        out_of_bounds_in_x = (x < 0) or x >= self.w
        out_of_bounds_in_y = (y < 0) or y >= self.h

        if out_of_bounds_in_x or out_of_bounds_in_y:
            return

        self.pixels.put_color_at(x, y, color)


@click.group()
def window_test():
    pass


@window_test.command()
def basic():
    import types

    glyph_w = 8
    glyph_h = 15

    def draw_text(self, x, y, text, fg_color, bg_color):
        x_pos = x
        y_pos = y
        print(f"{x_pos, y_pos}")
        for char in text:
            if char == "\n":
                x_pos = x
                y_pos += glyph_h
                continue

            glyph = fetch_glyph(char)
            self.draw_glyph(
                x_pos,
                y_pos,
                glyph,
                glyph_w,
                glyph_h,
                fg_color,
                bg_color,
            )
            x_pos += glyph_w

    def render_coords(self, event):
        self.clear()
        if event.type == sdl2.SDL_MOUSEMOTION:
            x = event.motion.x
            y = event.motion.y
            self.draw_text(
                x,
                y,
                f"({x},{y})",
                Color.from_int(0xA52A2A),
                Color.from_int(0x000000),
            )
        self.redraw()

    w = Window("basic window test", start_on_create=False)
    w.handle_mouse = types.MethodType(render_coords, w)
    w.draw_text = types.MethodType(draw_text, w)
    w.run()


@window_test.command()
def text():
    import types

    def draw_text_on_input(self, event):
        self.clear()
        self.draw_glyph(
            self.w // 2,
            self.h // 2,
            fetch_glyph(event.text.text),
            8,
            15,
            BLACK,
            PALE_YELLOW,
        )
        self.redraw()

    w = Window(
        "text window test",
        background=PALE_YELLOW,
        start_on_create=False,
    )
    w.handle_text = types.MethodType(draw_text_on_input, w)
    w.run()


@window_test.command()
@click.option("--size", type=(int, int))
@click.argument("image-location")
def image(image_location, size):
    w, h = None, None
    if size:
        w, h = size

    if image_location.startswith("http"):
        img = ImageForm.from_url(image_location, width=w, height=h)
    else:
        img = ImageForm.from_path(image_location, width=w, height=h)

    w = Window("image window test", start_on_create=False)
    w.draw_image(0, 0, img)
    w.run()
