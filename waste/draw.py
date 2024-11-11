import ctypes

import requests

from dataclasses import dataclass
from enum import Enum

from PIL import Image

from waste.debug import debugmethod


def sign(val):
    if val > 0:
        return 1
    if val < 0:
        return -1
    return 0


class OutOfBoundsError(Exception):
    """Raised when trying to access a location outside a form."""


@dataclass
class Point:
    x: int
    y: int

    @property
    def coordinates(self):
        return (self.x, self.y)

    def clone(self):
        return Point(self.x, self.y)


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

    def clone(self):
        return Rectangle(self.origin.clone(), self.corner.clone())


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

    def bitblt(self, src, src_rect, destination, op=Operation.STORE, clip_rect=None):
        """Take bits from the rectangle `src_rect` in source form `src` and
        copy them to a congruent rectangle in `self` with origin in
        `destination` according to operation `op`.

        An optional clipping rectangle `clip_rect` may be provided to clip the
        destination region."""

        if clip_rect is None:
            clip_rect = Rectangle(
                origin=Point(self.x, self.y),
                corner=Point(self.x + self.w, self.y + self.h),
            )

        self.clip_range(src, src_rect, destination, clip_rect)
        # self.check_overlap()  # TODO implement
        self.copy_bits(src, src_rect, destination, op)

    def draw_line(self, p0, p1, brush, op=Operation.STORE, clip_rect=None):
        # draw top to bottom or left to right
        # if points are in reverse direction, swap them
        from_x, from_y = p0.coordinates
        to_x, to_y = p1.coordinates

        is_forward = ((from_y == to_y) and (from_x < to_x)) or (from_y < to_y)
        if not is_forward:
            from_x, to_x = to_x, from_x
            from_y, to_y = to_y, from_y

        rect = brush.rect.clone()
        dest = Point(from_x, from_y)
        clip_rect = (clip_rect or self.rect.clone())

        if brush is None:
            dest = Point(from_x, from_y)

        x_delta = to_x - from_x
        y_delta = to_y - from_y

        dx = sign(x_delta)
        dy = sign(y_delta)
        px = abs(y_delta)
        py = abs(x_delta)

        if py > px:
            # more horizontal
            p = py // 2
            for i in range(0, py):
                dest.x += dx
                p = p - px
                if p < 0:
                    dest.y += dy
                    p += py
                if i < py:
                    # print(f'drawing at x={dest.x},y={dest.y}')
                    # FIXME this should be a call to bitblt
                    self.copy_bits(brush, rect, dest, op)
        else:
            # more vertical
            p = px // 2
            for i in range(0, px):
                dest.y += dy
                p = p - py
                if p < 0:
                    dest.x += dx
                    p += px
                if i < px:
                    # print(f'drawing at x={dest.x},y={dest.y}')
                    # FIXME this should be a call to bitblt
                    self.copy_bits(brush, rect, dest, op)

        # draw the first point
        if is_forward:
            self.copy_bits(brush, rect, p0, op)
        else:
            self.copy_bits(brush, rect, p1, op)

    def draw_rectangle(self, origin, corner, brush, op=Operation.STORE, clip_rect=None):
        top_right = Point(corner.x, origin.y)
        bottom_left = Point(origin.x, corner.y)
        self.draw_line(origin, top_right, brush, op)    # top side
        self.draw_line(top_right, corner, brush, op)    # right side
        self.draw_line(corner, bottom_left, brush, op)  # bottom side
        self.draw_line(bottom_left, origin, brush, op)  # left side

    def clip_range(self, src, src_rect, destination, clip_rect):
        # if clipping rect is outside the destination form
        # we discard the region that is out of bounds

        # left side
        if clip_rect.origin.x < 0:
            clip_rect.origin.x = 0

        # right side.
        if clip_rect.corner.x > self.rect.corner.x:
            clip_rect.corner.x = self.rect.corner.x

        # top
        if clip_rect.origin.y < 0:
            clip_rect.origin.y = 0

        # bottom
        if clip_rect.corner.y > self.rect.corner.y:
            clip_rect.corner.y = self.rect.corner.y

        # clip and adjust src_rect
        # in X
        if destination.x < clip_rect.origin.x:
            src_rect.origin.x = src_rect.origin.x + (clip_rect.origin.x - destination.x)
            destination.x = clip_rect.origin.x

        if src_rect.corner.x > clip_rect.corner.x:
            src_rect.corner.x = clip_rect.corner.x

        # in Y
        if destination.y < clip_rect.origin.y:
            src_rect.origin.y = src_rect.origin.y + (clip_rect.origin.y - destination.y)
            destination.y = clip_rect.origin.y

        if src_rect.corner.y > clip_rect.corner.y:
            src_rect.corner.y = clip_rect.corner.y

        if src is None:
            return

        # adjust source rectangle
        # in X
        if src_rect.origin.x < 0:
            destination.x = destination.x - src_rect.origin.x
            src_rect.origin.x = 0

        if src_rect.corner.x > src.rect.corner.x:
            src_rect.corner.x = src.rect.corner.x

        # in Y
        if src_rect.origin.y < 0:
            destination.y = destination.y - src_rect.origin.y
            src_rect.origin.y = 0

        if src_rect.corner.y > src.rect.corner.y:
            src_rect.corner.y = src.rect.corner.y

    def copy_bits(self, src, src_rect, destination, op):
        src_row = src.y
        dst_row = destination.y

        while src_row < src_rect.corner.y:
            self.merge(src, src_rect.x, destination.x, src_row, dst_row, src_rect.w, op)
            src_row += 1
            dst_row += 1

    def merge(self, src, src_x, dst_x, src_row, dst_row, row_width, op):
        src_bytes = src.row_bytes(src_x, src_row, row_width)
        dst_bytes = self.row_bytes(dst_x, dst_row, row_width)

        match op:
            case Operation.STORE:
                self.put_row_bytes(dst_x, dst_row, src_bytes)
            case Operation.OR:
                merged = bytearray(s | d for s, d in zip(src_bytes, dst_bytes))
                self.put_row_bytes(dst_x, dst_row, merged)
            case Operation.AND:
                merged = bytearray(s & d for s, d in zip(src_bytes, dst_bytes))
                self.put_row_bytes(dst_x, dst_row, merged)
            case Operation.XOR:
                merged = bytearray(s ^ d for s, d in zip(src_bytes, dst_bytes))
                self.put_row_bytes(dst_x, dst_row, merged)
            case Operation.CLR:
                self.put_row_bytes(dst_x, dst_row, bytes(len(dst_bytes) * [0x00]))
            case _:
                raise RuntimeError(f"Unsupported operation {op=}!")

    def color_at(self, x, y):
        _0th, _nth = self._pixel_bytes_range_at_point(x, y)
        pixel_bytes = self.bitmap[_0th:_nth]
        return Color.from_values(pixel_bytes)

    def put_color_at(self, x, y, color):
        _0th, _nth = self._pixel_bytes_range_at_point(x, y)
        self.bitmap[_0th:_nth] = color.values

    def row_bytes(self, x, y, pixel_count):
        byte_0 = (y * (self.w * self.depth)) + (x * self.depth)
        byte_n = byte_0 + (self.depth * (pixel_count))
        return self.bitmap[byte_0:byte_n]

    def put_row_bytes(self, x, y, row_bytes):
        if (x < 0) or (y < 0):
            return

        if x + (len(row_bytes) // self.depth) > self.w:
            pixel_count = len(row_bytes) // self.depth
            stop = x + pixel_count
            pixels_to_remove = stop - self.w
            bytes_to_remove = pixels_to_remove * self.depth
            row_bytes = row_bytes[:-bytes_to_remove]

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
