import ctypes

import requests

from dataclasses import dataclass
from enum import Enum

from PIL import Image


class OutOfBoundsError(Exception):
    """Raised when trying to access a location outside a form."""


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Rectangle:
    origin: Point
    corner: Point

    @property
    def x(self):
        return self.origin.x

    @x.setter
    def x(self, x):
        self.origin.x = x

    @property
    def y(self):
        return self.origin.y

    @y.setter
    def y(self, y):
        self.origin.y = y

    @property
    def w(self):
        return self.corner.x - self.origin.x

    @w.setter
    def w(self, w):
        self.corner.x = self.x + w

    @property
    def h(self):
        return self.corner.y - self.origin.y

    @h.setter
    def h(self, h):
        self.corner.y = self.y + h


class Operation(Enum):
    STORE = "STORE"  # dst = src
    OR = "OR"  # dst = dst | src
    AND = "AND"  # dst = dst & src
    XOR = "XOR"  # dst = dst ^ src
    CLR = "CLR"  # dst = dst & ~src


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


class Form:
    def __init__(self, x, y, w, h, bitmap=None):
        self.rect = Rectangle(origin=Point(x, y), corner=Point(x + w, y + h))

        if bitmap is None:
            bitmap = bytearray(self.w * self.h * self.depth * [0x00])
        self.bitmap = bitmap

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, x):
        self.rect.x = x

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, y):
        self.rect.y = y

    @property
    def w(self):
        return self.rect.w

    @property
    def h(self):
        return self.rect.h

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
