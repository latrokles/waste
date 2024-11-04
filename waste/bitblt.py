from dataclasses import dataclass
from enum import Enum


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Rectangle:
    origin: Point
    corner: Point

    @property
    def w(self):
        return self.corner.x - self.origin.x

    @property
    def h(self):
        return self.corner.y - self.origin.y


class Bitmap:
    def __init__(self, x, y, w, h, depth, data = None):
        self.rect = Rectangle(Point(x, y), Point(x+w, y+h))
        self.w = w
        self.depth = depth

        if data is None:
            data = bytearray(w * h * depth * [0x00])
        self.data = data


class Operation(Enum):
    STORE = "STORE"  # dst = src
    OR = "OR"        # dst = dst | src
    AND = "AND"      # dst = dst & src
    XOR = "XOR"      # dst = dst ^ src
    CLR = "CLR"      # dst = dst & ~src


def bitblt(src_form, dst_form, src_rect, dst_point, clip_rect=None, op=Operation.STORE):
    """Take bits from the rectangle `src_rect` in `src` form and copy them to a
    congruent rectangle in `dst` form with its origin in `dst_point` according
    to the operation `op`."""

    if clip_rect is None:
        clip_rect = Rectangle(Point(0, 0), Point(dst_form.w, dst_form.h))

    clip_range(src_form, dst_form, src_rect, dst_point, clip_rect)
    check_overlap()  # TODO
    copy_loop(src_form, dst_form, src_rect, dst_point, clip_rect, op)


def clip_range(src_form, dst_form, src_rect, dst_point, clip_rect):
    # if clipping rect is outside the destination form
    # we discard the region that is out of bounds

    # left side
    if clip_rect.origin.x < 0:
        clip_rect.origin.x = 0

    # right side.
    if clip_rect.corner.x > dst_form.rect.corner.x:
        clip_rect.corner.x = dst_form.rect.corner.x

    # top
    if clip_rect.origin.y < 0:
        clip_rect.origin.y = 0

    # bottom
    if clip_rect.corner.y > dst_form.rect.corner.y:
        clip_rect.corner.y = dst_form.rect.corner.y

    # clip and adjust src_rect
    # in X
    if dst_point.x < clip_rect.origin.x:
        src_rect.origin.x = src_rect.origin.x + (clip_rect.origin.x - dst_point.x)
        dst_point.x = clip_rect.origin.x

    if src_rect.corner.x > clip_rect.corner.x:
        src_rect.corner.x = clip_rect.corner.x

    # in Y
    if dst_point.y < clip_rect.origin.y:
        src_rect.origin.y = src_rect.origin.y + (clip_rect.origin.y - dst_point.y)
        dst_point.y = clip_rect.origin.y

    if src_rect.corner.y > clip_rect.corner.y:
        src_rect.corner.y = clip_rect.corner.y

    if src_form is None:
        return

    # adjust source rectangle
    # in X
    if src_rect.origin.x < 0:
        dst_point.x = dst_point.x - src_rect.origin.x
        src_rect.origin.x = 0

    if src_rect.corner.x > src_form.rect.corner.x:
        src_rect.corner.x = src_form.rect.corner.x

    # in Y
    if src_rect.origin.y < 0:
        dst_point.y = dst_point.y - src_rect.origin.y
        src_rect.origin.y = 0

    if src_rect.corner.y > src_form.rect.corner.y:
        src_rect.corner.y = src_form.rect.corner.y


def check_overlap():
    return


def copy_bits(src_form, dst_form, src_rect, dst_point, op):
    src_row = src_rect.origin.y
    dst_row = dst_point.y

    while src_row < src_rect.corner.y:
        merge(
            src_form,
            dst_form,
            src_rect.origin.x,
            dst_point.x,
            src_row,
            dst_row,
            src_rect.w,
            op,
        )

        src_row += 1
        dst_row += 1


def merge(src_form, dst_form, src_x, dst_x, src_row, dst_row, row_width, op):
    src_bytes = src_form.row_bytes(src_x, src_row, row_width)
    dst_bytes = dst_form.row_bytes(dst_x, dst_row, row_width)

    match op:
        case Operation.STORE:
            dst_form.put_row_bytes(dst_x, dst_row, src_bytes)
        case Operation.OR:
            merged = bytearray(s | d for s, d in zip(src_bytes, dst_bytes))
            dst_form.put_row_bytes(dst_x, dst_row, merged)
        case Operation.AND:
            merged = bytearray(s & d for s, d in zip(src_bytes, dst_bytes))
            dst_form.put_row_bytes(dst_x, dst_row, merged)
        case Operation.XOR:
            merged = bytearray(s ^ d for s, d in zip(src_bytes, dst_bytes))
            dst_form.put_row_bytes(dst_x, dst_row, merged)
        case Operation.CLR:
            dst_form.put_row_bytes(dst_x, dst_row, bytes(len(dst_bytes)*[0x00]))
        case _:
            raise RuntimeError(f"Unsupported operation {op=}!")
