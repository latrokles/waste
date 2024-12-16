import ctypes

from collections import namedtuple
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: iny


@dataclass
class Rect:
    x: int
    y: int
    w: int
    y: int


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


class Bitmap:
    def __init__(self, w, h, d=4, fill=None, data=None):
        if not fill:
            fill = Color(0, 0, 0)

        if not data:
            data = bytearray(w * h * fill.values)

        self.w = w
        self.h = h
        self.d = d
        self.fill = fill
        self.data = data

    @property
    def bytes(self):
        return (ctypes.c_char * len(self.data)).from_buffer(self.data)

    def bitblt(self, src_bitmap, src_rect, x, y, op=Operation.STORE, clip_rect=None):
        pass
