'''
This corresponds to:
https://github.com/9fans/plan9port/blob/master/font/fixed/unicode.8x13.font

For license see:
https://github.com/9fans/plan9port/blob/master/font/fixed/README
'''

from waste.debug import debugfunc

GLYPH_W = 8
GLYPH_H = 15
GLYPHS = [
    [0x00,0x18,0x3e,0x0f,0x87,0xff,0x8f,0x0f,0x1f,0x0e,0x1c,0x1c,0x00,0x00,0x00],  # 0 (nonprintable)
    [0x00,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff],  # 1 (nonprintable)
    [0x00,0x70,0x80,0xf0,0x10,0xe0,0x1c,0x08,0x08,0x08,0x04,0x02,0x03,0x05,0x04],  # 2 (nonprintable)
    [0x00,0xe0,0x80,0xe0,0x80,0xe0,0x1c,0x08,0x08,0x08,0x04,0x02,0x03,0x05,0x04],  # 3 (nonprintable)
    [0x00,0xe0,0x80,0xe0,0x80,0xe0,0x18,0x24,0x24,0x18,0x03,0x01,0x01,0x01,0x01],  # 4 (nonprintable)
    [0x00,0xe0,0x80,0xe0,0x80,0xe0,0x12,0x1a,0x16,0x12,0x03,0x04,0x04,0x05,0x03],  # 5 (nonprintable)
    [0x00,0x60,0x90,0xf0,0x90,0x90,0x0c,0x10,0x10,0x0c,0x02,0x03,0x03,0x02,0x02],  # 6 (nonprintable)
    [0x00,0x00,0x00,0x08,0x1c,0x3e,0x36,0x36,0x36,0x63,0xc1,0xff,0x1c,0x00,0x00],  # 7 (nonprintable)
    [0x00,0x00,0x00,0x70,0x48,0x70,0x48,0x70,0x07,0x08,0x06,0x01,0x0e,0x00,0x00],  # 8 (nonprintable)
    [0x00,0x00,0x00,0x48,0x48,0x78,0x48,0x48,0x07,0x02,0x02,0x02,0x02,0x00,0x00],  # 9 (nonprintable)
    [0x00,0x00,0x00,0x40,0x40,0x40,0x40,0x70,0x0e,0x08,0x0e,0x08,0x08,0x00,0x00],  # 10 (nonprintable)
    [0x00,0x00,0x00,0x48,0x48,0x48,0x30,0x30,0x07,0x02,0x02,0x02,0x02,0x00,0x00],  # 11 (nonprintable)
    [0x00,0x00,0x00,0x70,0x40,0x70,0x40,0x40,0x0e,0x08,0x0e,0x08,0x08,0x00,0x00],  # 12 (nonprintable)
    [0x00,0x00,0x00,0x70,0x90,0x80,0x90,0x60,0x00,0x1c,0x12,0x1e,0x14,0x12,0x00],  # 13 (nonprintable)
    [0x00,0x00,0x00,0x38,0x40,0x30,0x08,0x70,0x06,0x09,0x09,0x09,0x06,0x00,0x00],  # 14 (nonprintable)
    [0x00,0x00,0x00,0x38,0x40,0x30,0x08,0x70,0x07,0x02,0x02,0x02,0x07,0x00,0x00],  # 15 (nonprintable)
    [0x00,0xe0,0x90,0x90,0x90,0xe0,0x10,0x10,0x10,0x1c,0x03,0x02,0x03,0x02,0x03],  # 16 (nonprintable)
    [0x00,0xe0,0x90,0x90,0x90,0xe0,0x1c,0x24,0x20,0x20,0x1d,0x03,0x01,0x01,0x01],  # 17 (nonprintable)
    [0x00,0xe0,0x90,0x90,0x90,0xe0,0x1c,0x24,0x20,0x20,0x1b,0x04,0x01,0x02,0x07],  # 18 (nonprintable)
    [0x00,0xe0,0x90,0x90,0x90,0xe0,0x1c,0x24,0x20,0x20,0x1b,0x00,0x03,0x00,0x03],  # 19 (nonprintable)
    [0x00,0xe0,0x90,0x90,0x90,0xe0,0x1c,0x24,0x20,0x20,0x19,0x03,0x05,0x0f,0x01],  # 20 (nonprintable)
    [0x00,0x90,0xd0,0xb0,0x90,0x90,0x0c,0x12,0x1e,0x12,0x04,0x05,0x06,0x05,0x04],  # 21 (nonprintable)
    [0x00,0x70,0x80,0x60,0x10,0xe0,0x22,0x14,0x08,0x08,0x04,0x06,0x05,0x04,0x04],  # 22 (nonprintable)
    [0x00,0xe0,0x80,0xe0,0x80,0xe0,0x1c,0x08,0x08,0x08,0x07,0x04,0x07,0x04,0x07],  # 23 (nonprintable)
    [0x00,0x70,0x90,0x80,0x80,0x70,0x0c,0x12,0x1e,0x12,0x04,0x06,0x05,0x04,0x04],  # 24 (nonprintable)
    [0x00,0x00,0x00,0xe0,0x80,0xe0,0x80,0xe0,0x11,0x1b,0x15,0x15,0x11,0x00,0x00],  # 25 (nonprintable)
    [0x00,0x70,0x80,0x60,0x10,0xe0,0x24,0x24,0x24,0x18,0x07,0x04,0x07,0x04,0x07],  # 26 (nonprintable)
    [0x00,0xe0,0x80,0xe0,0x80,0xe0,0x1c,0x20,0x18,0x04,0x3b,0x04,0x04,0x04,0x03],  # 27 (nonprintable)
    [0x00,0x00,0x00,0x70,0x40,0x70,0x40,0x40,0x0e,0x10,0x0c,0x02,0x1c,0x00,0x00],  # 28 (nonprintable)
    [0x00,0x00,0x00,0x38,0x40,0x58,0x48,0x38,0x07,0x08,0x06,0x01,0x0e,0x00,0x00],  # 29 (nonprintable)
    [0x00,0x00,0x00,0x70,0x48,0x70,0x50,0x48,0x07,0x08,0x06,0x01,0x0e,0x00,0x00],  # 30 (nonprintable)
    [0x00,0x00,0x00,0x48,0x48,0x48,0x48,0x30,0x07,0x08,0x06,0x01,0x0e,0x00,0x00],  # 31 (nonprintable)
    [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],  # 32 ( )
    [0x00,0x00,0x00,0x18,0x18,0x18,0x18,0x18,0x18,0x08,0x00,0x18,0x18,0x00,0x00],  # 33 (!)
    [0x00,0x00,0x12,0x12,0x12,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],  # 34 (")
    [0x00,0x00,0x00,0x24,0x24,0x24,0xff,0x24,0x24,0xff,0x24,0x24,0x24,0x00,0x00],  # 35 (#)
    [0x00,0x00,0x04,0x3e,0x65,0x64,0x74,0x3c,0x1e,0x17,0x13,0x53,0x3e,0x10,0x00],  # 36 ($)
    [0x00,0x00,0x00,0x38,0x6c,0x6d,0x3a,0x04,0x08,0x17,0x2d,0x4d,0x07,0x00,0x00],  # 37 (%)
    [0x00,0x00,0x00,0x38,0x6c,0x6c,0x68,0x33,0x5b,0xca,0xcc,0xee,0x73,0x00,0x00],  # 38 (&)
    [0x00,0x00,0x1c,0x1c,0x04,0x18,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],  # 39 (')
    [0x00,0x00,0x06,0x0c,0x18,0x18,0x30,0x30,0x30,0x30,0x18,0x18,0x0c,0x06,0x00],  # 40 (()
    [0x00,0x00,0x30,0x18,0x0c,0x0c,0x06,0x06,0x06,0x06,0x0c,0x0c,0x18,0x30,0x00],  # 41 ())
    [0x00,0x00,0x00,0x08,0x2a,0x1c,0x2a,0x08,0x00,0x00,0x00,0x00,0x00,0x00,0x00],  # 42 (*)
    [0x00,0x00,0x00,0x00,0x00,0x08,0x08,0x08,0x7f,0x08,0x08,0x08,0x00,0x00,0x00],  # 43 (+)
    [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1c,0x1c,0x04,0x18],  # 44 (,)
    [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x7f,0x00,0x00,0x00,0x00,0x00,0x00],  # 45 (-)
    [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1c,0x1c,0x00,0x00],  # 46 (.)
    [0x00,0x00,0x03,0x03,0x06,0x06,0x0c,0x0c,0x18,0x18,0x30,0x30,0x60,0x60,0x00],  # 47 (/)
    [0x00,0x00,0x00,0x1c,0x36,0x63,0x63,0x63,0x63,0x63,0x63,0x36,0x1c,0x00,0x00],  # 48 (0)
    [0x00,0x00,0x00,0x0c,0x1c,0x2c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x00,0x00],  # 49 (1)
    [0x00,0x00,0x00,0x3e,0x67,0x03,0x03,0x06,0x0c,0x18,0x30,0x7f,0x7f,0x00,0x00],  # 50 (2)
    [0x00,0x00,0x00,0x3e,0x67,0x03,0x06,0x1c,0x06,0x03,0x03,0x67,0x3e,0x00,0x00],  # 51 (3)
    [0x00,0x00,0x00,0x06,0x0e,0x16,0x26,0x46,0x7f,0x7f,0x06,0x06,0x06,0x00,0x00],  # 52 (4)
    [0x00,0x00,0x00,0x7f,0x7f,0x40,0x40,0x7e,0x07,0x03,0x03,0x66,0x3c,0x00,0x00],  # 53 (5)
    [0x00,0x00,0x00,0x1e,0x33,0x60,0x6c,0x76,0x63,0x63,0x63,0x36,0x1c,0x00,0x00],  # 54 (6)
    [0x00,0x00,0x00,0x7f,0x7f,0x03,0x06,0x0c,0x18,0x18,0x30,0x30,0x30,0x00,0x00],  # 55 (7)
    [0x00,0x00,0x00,0x3e,0x63,0x63,0x72,0x3c,0x3e,0x67,0x63,0x63,0x3e,0x00,0x00],  # 56 (8)
    [0x00,0x00,0x00,0x1c,0x36,0x63,0x63,0x63,0x37,0x1b,0x03,0x66,0x3c,0x00,0x00],  # 57 (9)
    [0x00,0x00,0x00,0x00,0x00,0x00,0x18,0x18,0x00,0x00,0x00,0x18,0x18,0x00,0x00],  # 58 (:)
    [0x00,0x00,0x00,0x00,0x00,0x00,0x18,0x18,0x00,0x00,0x00,0x18,0x18,0x08,0x10],  # 59 (;)
    [0x00,0x00,0x00,0x00,0x00,0x06,0x0c,0x18,0x30,0x18,0x0c,0x06,0x00,0x00,0x00],  # 60 (<)
    [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x7f,0x00,0x7f,0x00,0x00,0x00,0x00,0x00],  # 61 (=)
    [0x00,0x00,0x00,0x00,0x00,0x30,0x18,0x0c,0x06,0x0c,0x18,0x30,0x00,0x00,0x00],  # 62 (>)
    [0x00,0x00,0x00,0x3e,0x63,0x03,0x03,0x0e,0x18,0x18,0x00,0x18,0x18,0x00,0x00],  # 63 (?)
    [0x00,0x00,0x00,0x1c,0x62,0x43,0x8f,0x9b,0x9b,0x9b,0x4d,0x60,0x1e,0x00,0x00],  # 64 (@)
    [0x00,0x00,0x00,0x18,0x18,0x2c,0x2c,0x66,0x46,0xfe,0xc3,0xc3,0xc3,0x00,0x00],  # 65 (A)
    [0x00,0x00,0x00,0x7c,0x66,0x66,0x64,0x78,0x64,0x66,0x66,0x66,0x7c,0x00,0x00],  # 66 (B)
    [0x00,0x00,0x00,0x1e,0x33,0x60,0x60,0x60,0x60,0x60,0x60,0x33,0x1e,0x00,0x00],  # 67 (C)
    [0x00,0x00,0x00,0x7c,0x66,0x63,0x63,0x63,0x63,0x63,0x63,0x66,0x7c,0x00,0x00],  # 68 (D)
    [0x00,0x00,0x00,0x7e,0x60,0x60,0x60,0x7c,0x60,0x60,0x60,0x60,0x7e,0x00,0x00],  # 69 (E)
    [0x00,0x00,0x00,0x7e,0x60,0x60,0x60,0x60,0x7e,0x60,0x60,0x60,0x60,0x00,0x00],  # 70 (F)
    [0x00,0x00,0x00,0x1e,0x33,0x60,0x60,0x60,0x63,0x63,0x63,0x33,0x1f,0x00,0x00],  # 71 (G)
    [0x00,0x00,0x00,0x63,0x63,0x63,0x63,0x7f,0x63,0x63,0x63,0x63,0x63,0x00,0x00],  # 72 (H)
    [0x00,0x00,0x00,0x7e,0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x7e,0x00,0x00],  # 73 (I)
    [0x00,0x00,0x00,0x3e,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x0c,0x78,0x00,0x00],  # 74 (J)
    [0x00,0x00,0x00,0x63,0x66,0x64,0x68,0x78,0x6c,0x66,0x66,0x63,0x63,0x00,0x00],  # 75 (K)
    [0x00,0x00,0x00,0x60,0x60,0x60,0x60,0x60,0x60,0x60,0x60,0x60,0x7e,0x00,0x00],  # 76 (L)
    [0x00,0x00,0x00,0xc3,0xc3,0xe7,0xe7,0xef,0xbb,0xbb,0x93,0x83,0x83,0x00,0x00],  # 77 (M)
    [0x00,0x00,0x00,0x61,0x71,0x71,0x59,0x59,0x4d,0x4d,0x47,0x47,0x43,0x00,0x00],  # 78 (N)
    [0x00,0x00,0x00,0x3c,0x66,0xc3,0xc3,0xc3,0xc3,0xc3,0xc3,0x66,0x3c,0x00,0x00],  # 79 (O)
    [0x00,0x00,0x00,0x7e,0x63,0x63,0x63,0x66,0x7c,0x60,0x60,0x60,0x60,0x00,0x00],  # 80 (P)
    [0x00,0x00,0x00,0x3c,0x66,0xc3,0xc3,0xc3,0xc3,0xc3,0xc3,0x66,0x3c,0x06,0x03],  # 81 (Q)
    [0x00,0x00,0x00,0x7c,0x66,0x66,0x64,0x78,0x6c,0x66,0x66,0x63,0x63,0x00,0x00],  # 82 (R)
    [0x00,0x00,0x00,0x3e,0x63,0x60,0x70,0x3c,0x0e,0x07,0x03,0x63,0x3e,0x00,0x00],  # 83 (S)
    [0x00,0x00,0x00,0xff,0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x00,0x00],  # 84 (T)
    [0x00,0x00,0x00,0x63,0x63,0x63,0x63,0x63,0x63,0x63,0x63,0x36,0x1c,0x00,0x00],  # 85 (U)
    [0x00,0x00,0x00,0xc3,0xc3,0xc3,0x62,0x62,0x66,0x34,0x34,0x18,0x18,0x00,0x00],  # 86 (V)
    [0x00,0x00,0x00,0xc3,0xc3,0xdb,0xdb,0xdb,0xda,0x6e,0x6e,0x66,0x66,0x00,0x00],  # 87 (W)
    [0x00,0x00,0x00,0x63,0x63,0x63,0x32,0x1c,0x1c,0x26,0x63,0x63,0x63,0x00,0x00],  # 88 (X)
    [0x00,0x00,0x00,0xc3,0xc3,0x62,0x66,0x34,0x18,0x18,0x18,0x18,0x18,0x00,0x00],  # 89 (Y)
    [0x00,0x00,0x00,0x7f,0x03,0x06,0x0c,0x0c,0x18,0x30,0x30,0x60,0x7f,0x00,0x00],  # 90 (Z)
    [0x00,0x00,0x3e,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x3e,0x00],  # 91 ([)
    [0x00,0x00,0x60,0x60,0x30,0x30,0x18,0x18,0x0c,0x0c,0x06,0x06,0x03,0x03,0x00],  # 92 (\)
    [0x00,0x00,0x3e,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x3e,0x00],  # 93 (])
    [0x00,0x00,0x00,0x00,0x0c,0x0c,0x1e,0x12,0x33,0x21,0x21,0x00,0x00,0x00,0x00],  # 94 (^)
    [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xff,0x00],  # 95 (_)
    [0x00,0x00,0x0c,0x10,0x1c,0x1c,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],  # 96 (`)
    [0x00,0x00,0x00,0x00,0x00,0x7c,0x06,0x06,0x7e,0xc6,0xc6,0xce,0x77,0x00,0x00],  # 97 (a)
    [0x00,0x00,0x60,0x60,0x60,0x6c,0x76,0x63,0x63,0x63,0x63,0x66,0x7c,0x00,0x00],  # 98 (b)
    [0x00,0x00,0x00,0x00,0x00,0x1e,0x31,0x60,0x60,0x60,0x60,0x31,0x1e,0x00,0x00],  # 99 (c)
    [0x00,0x00,0x03,0x03,0x03,0x1f,0x33,0x63,0x63,0x63,0x63,0x37,0x1b,0x00,0x00],  # 100 (d)
    [0x00,0x00,0x00,0x00,0x00,0x1e,0x33,0x63,0x7f,0x60,0x60,0x31,0x1e,0x00,0x00],  # 101 (e)
    [0x00,0x00,0x0f,0x18,0x18,0x18,0x7f,0x18,0x18,0x18,0x18,0x18,0x18,0x00,0x00],  # 102 (f)
    [0x00,0x00,0x00,0x00,0x00,0x1f,0x33,0x63,0x63,0x63,0x37,0x1b,0x03,0x66,0x3c],  # 103 (g)
    [0x00,0x00,0x60,0x60,0x60,0x6e,0x77,0x63,0x63,0x63,0x63,0x63,0x63,0x00,0x00],  # 104 (h)
    [0x00,0x00,0x0c,0x0c,0x00,0x7c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x00,0x00],  # 105 (i)
    [0x00,0x00,0x06,0x06,0x00,0x3e,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x7c],  # 106 (j)
    [0x00,0x00,0x60,0x60,0x60,0x63,0x62,0x64,0x78,0x6c,0x66,0x63,0x63,0x00,0x00],  # 107 (k)
    [0x00,0x00,0x7c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x00,0x00],  # 108 (l)
    [0x00,0x00,0x00,0x00,0x00,0xb6,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0x00,0x00],  # 109 (m)
    [0x00,0x00,0x00,0x00,0x00,0x6e,0x77,0x63,0x63,0x63,0x63,0x63,0x63,0x00,0x00],  # 110 (n)
    [0x00,0x00,0x00,0x00,0x00,0x1c,0x36,0x63,0x63,0x63,0x63,0x36,0x1c,0x00,0x00],  # 111 (o)
    [0x00,0x00,0x00,0x00,0x00,0x6c,0x76,0x63,0x63,0x63,0x63,0x66,0x7c,0x60,0x60],  # 112 (p)
    [0x00,0x00,0x00,0x00,0x00,0x1f,0x33,0x63,0x63,0x63,0x63,0x37,0x1b,0x03,0x03],  # 113 (q)
    [0x00,0x00,0x00,0x00,0x00,0x33,0x37,0x39,0x30,0x30,0x30,0x30,0x30,0x00,0x00],  # 114 (r)
    [0x00,0x00,0x00,0x00,0x00,0x3e,0x61,0x60,0x7c,0x1f,0x03,0x43,0x3e,0x00,0x00],  # 115 (s)
    [0x00,0x00,0x00,0x18,0x18,0x18,0x7f,0x18,0x18,0x18,0x18,0x18,0x0f,0x00,0x00],  # 116 (t)
    [0x00,0x00,0x00,0x00,0x00,0x63,0x63,0x63,0x63,0x63,0x63,0x77,0x3b,0x00,0x00],  # 117 (u)
    [0x00,0x00,0x00,0x00,0x00,0x63,0x63,0x63,0x36,0x36,0x34,0x1c,0x18,0x00,0x00],  # 118 (v)
    [0x00,0x00,0x00,0x00,0x00,0xc1,0xc1,0xc9,0xdd,0xdd,0x66,0x66,0x66,0x00,0x00],  # 119 (w)
    [0x00,0x00,0x00,0x00,0x00,0x63,0x63,0x32,0x1c,0x1c,0x26,0x63,0x63,0x00,0x00],  # 120 (x)
    [0x00,0x00,0x00,0x00,0x00,0x63,0x63,0x63,0x36,0x36,0x1c,0x18,0x18,0x30,0x30],  # 121 (y)
    [0x00,0x00,0x00,0x00,0x00,0x7f,0x03,0x06,0x0c,0x18,0x30,0x60,0x7f,0x00,0x00],  # 122 (z)
    [0x00,0x00,0x0f,0x18,0x18,0x0c,0x04,0x38,0x04,0x0c,0x18,0x18,0x18,0x0f,0x00],  # 123 ({)
    [0x00,0x00,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x00],  # 124 (|)
    [0x00,0x00,0x78,0x0c,0x0c,0x18,0x10,0x0e,0x10,0x18,0x0c,0x0c,0x0c,0x78,0x00],  # 125 (})
    [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x39,0x5d,0x4e,0x00,0x00,0x00,0x00,0x00],  # 126 (~)
    [0x00,0x55,0xaa,0x55,0xaa,0x55,0xaa,0x55,0xaa,0x55,0xaa,0x55,0xaa,0x00,0x00],  # 127 (nonprintable)
    [0xff,0x80,0x9c,0xb6,0x86,0x86,0x8c,0x98,0x98,0x80,0x98,0x98,0x80,0xff,0x00],  # 128 (nonprintable)
    [0xff,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0xff],  # 129 (nonprintable)
    [0xff,0x8f,0x7f,0x0f,0xef,0x1f,0xe3,0xf7,0xf7,0xf7,0xfb,0xfd,0xfc,0xfa,0xfb],  # 130 (nonprintable)
    [0xff,0x1f,0x7f,0x1f,0x7f,0x1f,0xe3,0xf7,0xf7,0xf7,0xfb,0xfd,0xfc,0xfa,0xfb],  # 131 (nonprintable)
    [0xff,0x1f,0x7f,0x1f,0x7f,0x1f,0xe7,0xdb,0xdb,0xe7,0xfc,0xfe,0xfe,0xfe,0xfe],  # 132 (nonprintable)
    [0xff,0x1f,0x7f,0x1f,0x7f,0x1f,0xed,0xe5,0xe9,0xed,0xfc,0xfb,0xfb,0xfa,0xfc],  # 133 (nonprintable)
    [0xff,0x9f,0x6f,0x0f,0x6f,0x6f,0xf3,0xef,0xef,0xf3,0xfd,0xfc,0xfc,0xfd,0xfd],  # 134 (nonprintable)
    [0xff,0xff,0xff,0xf7,0xe3,0xc1,0xc9,0xc9,0xc9,0x9c,0x3e,0x00,0xe3,0xff,0xff],  # 135 (nonprintable)
    [0xff,0xff,0xff,0x8f,0xb7,0x8f,0xb7,0x8f,0xf8,0xf7,0xf9,0xfe,0xf1,0xff,0xff],  # 136 (nonprintable)
    [0xff,0xff,0xff,0xb7,0xb7,0x87,0xb7,0xb7,0xf8,0xfd,0xfd,0xfd,0xfd,0xff,0xff],  # 137 (nonprintable)
    [0xff,0xff,0xff,0xbf,0xbf,0xbf,0xbf,0x8f,0xf1,0xf7,0xf1,0xf7,0xf7,0xff,0xff],  # 138 (nonprintable)
    [0xff,0xff,0xff,0xb7,0xb7,0xb7,0xcf,0xcf,0xf8,0xfd,0xfd,0xfd,0xfd,0xff,0xff],  # 139 (nonprintable)
    [0xff,0xff,0xff,0x8f,0xbf,0x8f,0xbf,0xbf,0xf1,0xf7,0xf1,0xf7,0xf7,0xff,0xff],  # 140 (nonprintable)
    [0xff,0x8f,0x6f,0x7f,0x6f,0x9f,0xff,0xe3,0xed,0xe1,0xeb,0xed,0xff,0xff,0xff],  # 141 (nonprintable)
    [0xff,0xff,0xff,0xc7,0xbf,0xcf,0xf7,0x8f,0xf9,0xf6,0xf6,0xf6,0xf9,0xff,0xff],  # 142 (nonprintable)
    [0xff,0xff,0xff,0xc7,0xbf,0xcf,0xf7,0x8f,0xf8,0xfd,0xfd,0xfd,0xf8,0xff,0xff],  # 143 (nonprintable)
    [0xff,0x1f,0x6f,0x6f,0x6f,0x1f,0xef,0xef,0xef,0xe3,0xfc,0xfd,0xfc,0xfd,0xfc],  # 144 (nonprintable)
    [0xff,0x1f,0x6f,0x6f,0x6f,0x1f,0xe3,0xdb,0xdf,0xdf,0xe2,0xfc,0xfe,0xfe,0xfe],  # 145 (nonprintable)
    [0xff,0x1f,0x6f,0x6f,0x6f,0x1f,0xe3,0xdb,0xdf,0xdf,0xe4,0xfb,0xfe,0xfd,0xf8],  # 146 (nonprintable)
    [0xff,0x1f,0x6f,0x6f,0x6f,0x1f,0xe3,0xdb,0xdf,0xdf,0xe4,0xff,0xfc,0xff,0xfc],  # 147 (nonprintable)
    [0xff,0x1f,0x6f,0x6f,0x6f,0x1f,0xe3,0xdb,0xdf,0xdf,0xe6,0xfc,0xfa,0xf0,0xfe],  # 148 (nonprintable)
    [0xff,0x6f,0x2f,0x4f,0x6f,0x6f,0xf3,0xed,0xe1,0xed,0xfb,0xfa,0xf9,0xfa,0xfb],  # 149 (nonprintable)
    [0xff,0x8f,0x7f,0x9f,0xef,0x1f,0xdd,0xeb,0xf7,0xf7,0xfb,0xf9,0xfa,0xfb,0xfb],  # 150 (nonprintable)
    [0xff,0x1f,0x7f,0x1f,0x7f,0x1f,0xe3,0xf7,0xf7,0xf7,0xf8,0xfb,0xf8,0xfb,0xf8],  # 151 (nonprintable)
    [0xff,0x8f,0x6f,0x7f,0x7f,0x8f,0xf3,0xed,0xe1,0xed,0xfb,0xf9,0xfa,0xfb,0xfb],  # 152 (nonprintable)
    [0xff,0xff,0xff,0x1f,0x7f,0x1f,0x7f,0x1f,0xee,0xe4,0xea,0xea,0xee,0xff,0xff],  # 153 (nonprintable)
    [0xff,0x8f,0x7f,0x9f,0xef,0x1f,0xdb,0xdb,0xdb,0xe7,0xf8,0xfb,0xf8,0xfb,0xf8],  # 154 (nonprintable)
    [0xff,0x1f,0x7f,0x1f,0x7f,0x1f,0xe3,0xdf,0xe7,0xfb,0xc4,0xfb,0xfb,0xfb,0xfc],  # 155 (nonprintable)
    [0xff,0xff,0xff,0x8f,0xbf,0x8f,0xbf,0xbf,0xf1,0xef,0xf3,0xfd,0xe3,0xff,0xff],  # 156 (nonprintable)
    [0xff,0xff,0xff,0xc7,0xbf,0xa7,0xb7,0xc7,0xf8,0xf7,0xf9,0xfe,0xf1,0xff,0xff],  # 157 (nonprintable)
    [0xff,0xff,0xff,0x8f,0xb7,0x8f,0xaf,0xb7,0xf8,0xf7,0xf9,0xfe,0xf1,0xff,0xff],  # 158 (nonprintable)
    [0xff,0xff,0xff,0xb7,0xb7,0xb7,0xb7,0xcf,0xf8,0xf7,0xf9,0xfe,0xf1,0xff,0xff],  # 159 (nonprintable)
    [0xff,0x00,0xff,0x00,0xff,0x00,0xff,0x00,0xff,0x00,0xff,0x00,0xff,0x00,0x00],  # 160 (nonprintable)
    [0x00,0x00,0x00,0x00,0x00,0x18,0x18,0x00,0x10,0x18,0x18,0x18,0x18,0x18,0x18],  # 161 (¡)
    [0x00,0x00,0x04,0x04,0x1e,0x35,0x64,0x64,0x64,0x64,0x34,0x1f,0x04,0x04,0x00],  # 162 (¢)
    [0x00,0x00,0x00,0x0e,0x19,0x18,0x18,0x7e,0x18,0x18,0x18,0x30,0x7f,0x00,0x00],  # 163 (£)
    [0x00,0x00,0x00,0x80,0x41,0x3e,0x36,0x63,0x63,0x36,0x3e,0x41,0x80,0x00,0x00],  # 164 (¤)
    [0x00,0x00,0x00,0x61,0x61,0x31,0x33,0x1a,0x3f,0x0c,0x3f,0x0c,0x0c,0x00,0x00],  # 165 (¥)
    [0x00,0x00,0x0c,0x0c,0x0c,0x0c,0x0c,0x00,0x00,0x0c,0x0c,0x0c,0x0c,0x0c,0x00],  # 166 (¦)
    [0x00,0x00,0x00,0x3e,0x63,0x60,0x3c,0x66,0x63,0x33,0x1e,0x03,0x63,0x3e,0x00],  # 167 (§)
    [0x00,0x00,0x14,0x14,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],  # 168 (¨)
    [0x00,0x00,0x00,0x1e,0x21,0x4e,0x50,0x50,0x50,0x50,0x4e,0x21,0x1e,0x00,0x00],  # 169 (©)
    [0x00,0x00,0x00,0x3c,0x06,0x06,0x3e,0x66,0x6e,0x37,0x00,0x00,0x00,0x00,0x00],  # 170 (ª)
    [0x00,0x00,0x00,0x00,0x00,0x00,0x19,0x33,0x66,0x33,0x19,0x00,0x00,0x00,0x00],  # 171 («)
    [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x7f,0x01,0x01,0x00,0x00,0x00,0x00,0x00],  # 172 (¬)
    [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x3e,0x00,0x00,0x00,0x00,0x00,0x00],  # 173 (nonprintable)
    [0x00,0x00,0x00,0x1e,0x21,0x5c,0x52,0x5c,0x52,0x21,0x1e,0x00,0x00,0x00,0x00],  # 174 (®)
    [0x00,0x00,0x1c,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],  # 175 (¯)
    [0x00,0x00,0x00,0x1c,0x22,0x22,0x1c,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],  # 176 (°)
    [0x00,0x00,0x00,0x00,0x00,0x08,0x08,0x7f,0x08,0x08,0x00,0x7f,0x00,0x00,0x00],  # 177 (±)
    [0x00,0x00,0x00,0x3c,0x06,0x06,0x0c,0x18,0x30,0x3e,0x00,0x00,0x00,0x00,0x00],  # 178 (²)
    [0x00,0x00,0x00,0x3c,0x06,0x06,0x1c,0x06,0x06,0x3c,0x00,0x00,0x00,0x00,0x00],  # 179 (³)
    [0x00,0x00,0x06,0x18,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],  # 180 (´)
    [0x00,0x00,0x00,0x00,0x00,0x63,0x63,0x63,0x63,0x63,0x63,0x77,0x7b,0x60,0x60],  # 181 (µ)
    [0x00,0x00,0x00,0x1f,0x3d,0x3d,0x3d,0x3d,0x1d,0x05,0x05,0x05,0x05,0x05,0x00],  # 182 (¶)
    [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1c,0x1c,0x00,0x00,0x00,0x00,0x00],  # 183 (·)
    [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x08,0x30],  # 184 (¸)
    [0x00,0x00,0x00,0x38,0x58,0x18,0x18,0x18,0x18,0x7e,0x00,0x00,0x00,0x00,0x00],  # 185 (¹)
    [0x00,0x00,0x00,0x3e,0x63,0x63,0x63,0x63,0x63,0x3e,0x00,0x00,0x00,0x00,0x00],  # 186 (º)
    [0x00,0x00,0x00,0x00,0x00,0x00,0xcc,0x66,0x33,0x66,0xcc,0x00,0x00,0x00,0x00],  # 187 (»)
    [0x00,0x00,0x00,0x44,0xc4,0x48,0x48,0x53,0x55,0x29,0x2f,0x41,0x41,0x00,0x00],  # 188 (¼)
    [0x00,0x00,0x00,0x44,0xc4,0x48,0x48,0x50,0x57,0x10,0x13,0x24,0x27,0x00,0x00],  # 189 (½)
    [0x00,0x00,0x00,0xe4,0x24,0xc8,0x28,0xd3,0x15,0x29,0x2f,0x41,0x41,0x00,0x00],  # 190 (¾)
    [0x00,0x00,0x00,0x00,0x00,0x0c,0x0c,0x00,0x0c,0x0c,0x38,0x60,0x60,0x63,0x3e],  # 191 (¿)
    [0x30,0x0c,0x00,0x18,0x18,0x2c,0x2c,0x66,0x46,0xfe,0xc3,0xc3,0xc3,0x00,0x00],  # 192 (À)
    [0x0c,0x30,0x00,0x18,0x18,0x2c,0x2c,0x66,0x46,0xfe,0xc3,0xc3,0xc3,0x00,0x00],  # 193 (Á)
    [0x18,0x24,0x00,0x18,0x18,0x2c,0x2c,0x66,0x46,0xfe,0xc3,0xc3,0xc3,0x00,0x00],  # 194 (Â)
    [0x1a,0x2c,0x00,0x18,0x18,0x2c,0x2c,0x66,0x46,0xfe,0xc3,0xc3,0xc3,0x00,0x00],  # 195 (Ã)
    [0x24,0x24,0x00,0x18,0x18,0x2c,0x2c,0x66,0x46,0xfe,0xc3,0xc3,0xc3,0x00,0x00],  # 196 (Ä)
    [0x00,0x18,0x24,0x18,0x18,0x2c,0x2c,0x66,0x46,0xfe,0xc3,0xc3,0xc3,0x00,0x00],  # 197 (Å)
    [0x00,0x00,0x00,0x0f,0x1c,0x2c,0x2c,0x6f,0x4c,0x7c,0xcc,0xcc,0xcf,0x00,0x00],  # 198 (Æ)
    [0x00,0x00,0x00,0x1e,0x33,0x60,0x60,0x60,0x60,0x60,0x60,0x33,0x1e,0x04,0x18],  # 199 (Ç)
    [0x18,0x06,0x00,0x3f,0x30,0x30,0x30,0x3e,0x30,0x30,0x30,0x30,0x3f,0x00,0x00],  # 200 (È)
    [0x06,0x18,0x00,0x3f,0x30,0x30,0x30,0x3e,0x30,0x30,0x30,0x30,0x3f,0x00,0x00],  # 201 (É)
    [0x0c,0x12,0x00,0x3f,0x30,0x30,0x30,0x3e,0x30,0x30,0x30,0x30,0x3f,0x00,0x00],  # 202 (Ê)
    [0x12,0x12,0x00,0x3f,0x30,0x30,0x30,0x3e,0x30,0x30,0x30,0x30,0x3f,0x00,0x00],  # 203 (Ë)
    [0x30,0x0c,0x00,0x7e,0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x7e,0x00,0x00],  # 204 (Ì)
    [0x0c,0x30,0x00,0x7e,0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x7e,0x00,0x00],  # 205 (Í)
    [0x18,0x24,0x00,0x7e,0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x7e,0x00,0x00],  # 206 (Î)
    [0x24,0x24,0x00,0x7e,0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x7e,0x00,0x00],  # 207 (Ï)
    [0x00,0x00,0x00,0x7c,0x66,0x63,0x63,0xfb,0x63,0x63,0x63,0x66,0x7c,0x00,0x00],  # 208 (Ð)
    [0x1a,0x2c,0x00,0x61,0x71,0x71,0x59,0x59,0x4d,0x4d,0x47,0x47,0x43,0x00,0x00],  # 209 (Ñ)
    [0x30,0x0c,0x00,0x3c,0x66,0xc3,0xc3,0xc3,0xc3,0xc3,0xc3,0x66,0x3c,0x00,0x00],  # 210 (Ò)
    [0x0c,0x30,0x00,0x3c,0x66,0xc3,0xc3,0xc3,0xc3,0xc3,0xc3,0x66,0x3c,0x00,0x00],  # 211 (Ó)
    [0x18,0x24,0x00,0x3c,0x66,0xc3,0xc3,0xc3,0xc3,0xc3,0xc3,0x66,0x3c,0x00,0x00],  # 212 (Ô)
    [0x1a,0x2c,0x00,0x3c,0x66,0xc3,0xc3,0xc3,0xc3,0xc3,0xc3,0x66,0x3c,0x00,0x00],  # 213 (Õ)
    [0x24,0x24,0x00,0x3c,0x66,0xc3,0xc3,0xc3,0xc3,0xc3,0xc3,0x66,0x3c,0x00,0x00],  # 214 (Ö)
    [0x00,0x00,0x00,0x00,0x00,0x00,0x32,0x1c,0x08,0x1c,0x26,0x00,0x00,0x00,0x00],  # 215 (×)
    [0x00,0x00,0x00,0x3d,0x66,0xc7,0xcb,0xcb,0xd3,0xd3,0xe3,0x66,0xbc,0x00,0x00],  # 216 (Ø)
    [0x30,0x0c,0x00,0x63,0x63,0x63,0x63,0x63,0x63,0x63,0x63,0x36,0x1c,0x00,0x00],  # 217 (Ù)
    [0x06,0x18,0x00,0x63,0x63,0x63,0x63,0x63,0x63,0x63,0x63,0x36,0x1c,0x00,0x00],  # 218 (Ú)
    [0x0c,0x12,0x00,0x63,0x63,0x63,0x63,0x63,0x63,0x63,0x63,0x36,0x1c,0x00,0x00],  # 219 (Û)
    [0x14,0x14,0x00,0x63,0x63,0x63,0x63,0x63,0x63,0x63,0x63,0x36,0x1c,0x00,0x00],  # 220 (Ü)
    [0x0c,0x30,0x00,0xc3,0xc3,0x62,0x66,0x34,0x18,0x18,0x18,0x18,0x18,0x00,0x00],  # 221 (Ý)
    [0x00,0x00,0x00,0x60,0x60,0x7e,0x63,0x63,0x63,0x66,0x7c,0x60,0x60,0x00,0x00],  # 222 (Þ)
    [0x00,0x00,0x3c,0x66,0x66,0x64,0x6c,0x66,0x63,0x63,0x63,0x63,0x66,0x00,0x00],  # 223 (ß)
    [0x00,0x00,0x30,0x0c,0x00,0x7c,0x06,0x06,0x7e,0xc6,0xc6,0xce,0x77,0x00,0x00],  # 224 (à)
    [0x00,0x00,0x0c,0x30,0x00,0x7c,0x06,0x06,0x7e,0xc6,0xc6,0xce,0x77,0x00,0x00],  # 225 (á)
    [0x00,0x00,0x18,0x24,0x00,0x7c,0x06,0x06,0x7e,0xc6,0xc6,0xce,0x77,0x00,0x00],  # 226 (â)
    [0x00,0x00,0x34,0x58,0x00,0x7c,0x06,0x06,0x7e,0xc6,0xc6,0xce,0x77,0x00,0x00],  # 227 (ã)
    [0x00,0x00,0x28,0x28,0x00,0x7c,0x06,0x06,0x7e,0xc6,0xc6,0xce,0x77,0x00,0x00],  # 228 (ä)
    [0x00,0x00,0x18,0x24,0x18,0x7c,0x06,0x06,0x7e,0xc6,0xc6,0xce,0x77,0x00,0x00],  # 229 (å)
    [0x00,0x00,0x00,0x00,0x00,0x76,0x1b,0x1b,0x7f,0xd8,0xd8,0xdd,0x66,0x00,0x00],  # 230 (æ)
    [0x00,0x00,0x00,0x00,0x00,0x1e,0x31,0x60,0x60,0x60,0x60,0x31,0x1e,0x04,0x18],  # 231 (ç)
    [0x00,0x00,0x18,0x06,0x00,0x1e,0x33,0x63,0x7f,0x60,0x60,0x31,0x1e,0x00,0x00],  # 232 (è)
    [0x00,0x00,0x06,0x18,0x00,0x1e,0x33,0x63,0x7f,0x60,0x60,0x31,0x1e,0x00,0x00],  # 233 (é)
    [0x00,0x00,0x0c,0x12,0x00,0x1e,0x33,0x63,0x7f,0x60,0x60,0x31,0x1e,0x00,0x00],  # 234 (ê)
    [0x00,0x00,0x12,0x12,0x00,0x1e,0x33,0x63,0x7f,0x60,0x60,0x31,0x1e,0x00,0x00],  # 235 (ë)
    [0x00,0x00,0x18,0x06,0x00,0x7c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x00,0x00],  # 236 (ì)
    [0x00,0x00,0x06,0x18,0x00,0x7c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x00,0x00],  # 237 (í)
    [0x00,0x00,0x0c,0x12,0x00,0x7c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x00,0x00],  # 238 (î)
    [0x00,0x00,0x12,0x12,0x00,0x7c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x0c,0x00,0x00],  # 239 (ï)
    [0x00,0x00,0x76,0x18,0x6c,0x06,0x1e,0x37,0x63,0x63,0x63,0x36,0x1c,0x00,0x00],  # 240 (ð)
    [0x00,0x00,0x1a,0x2c,0x00,0x6e,0x77,0x63,0x63,0x63,0x63,0x63,0x63,0x00,0x00],  # 241 (ñ)
    [0x00,0x00,0x30,0x0c,0x00,0x1c,0x36,0x63,0x63,0x63,0x63,0x36,0x1c,0x00,0x00],  # 242 (ò)
    [0x00,0x00,0x06,0x18,0x00,0x1c,0x36,0x63,0x63,0x63,0x63,0x36,0x1c,0x00,0x00],  # 243 (ó)
    [0x00,0x00,0x0c,0x12,0x00,0x1c,0x36,0x63,0x63,0x63,0x63,0x36,0x1c,0x00,0x00],  # 244 (ô)
    [0x00,0x00,0x1a,0x2c,0x00,0x1c,0x36,0x63,0x63,0x63,0x63,0x36,0x1c,0x00,0x00],  # 245 (õ)
    [0x00,0x00,0x14,0x14,0x00,0x1c,0x36,0x63,0x63,0x63,0x63,0x36,0x1c,0x00,0x00],  # 246 (ö)
    [0x00,0x00,0x00,0x00,0x00,0x08,0x08,0x00,0x7f,0x00,0x08,0x08,0x00,0x00,0x00],  # 247 (÷)
    [0x00,0x00,0x00,0x00,0x00,0x1d,0x36,0x67,0x6b,0x6b,0x73,0x36,0x5c,0x00,0x00],  # 248 (ø)
    [0x00,0x00,0x30,0x0c,0x00,0x63,0x63,0x63,0x63,0x63,0x63,0x77,0x3b,0x00,0x00],  # 249 (ù)
    [0x00,0x00,0x06,0x18,0x00,0x63,0x63,0x63,0x63,0x63,0x63,0x77,0x3b,0x00,0x00],  # 250 (ú)
    [0x00,0x00,0x0c,0x12,0x00,0x63,0x63,0x63,0x63,0x63,0x63,0x77,0x3b,0x00,0x00],  # 251 (û)
    [0x00,0x00,0x14,0x14,0x00,0x63,0x63,0x63,0x63,0x63,0x63,0x77,0x3b,0x00,0x00],  # 252 (ü)
    [0x00,0x00,0x06,0x18,0x00,0x63,0x63,0x63,0x36,0x36,0x1c,0x18,0x18,0x30,0x30],  # 253 (ý)
    [0x00,0x00,0x00,0x60,0x60,0x6c,0x76,0x63,0x63,0x63,0x63,0x66,0x7c,0x60,0x60],  # 254 (þ)
    [0x00,0x00,0x14,0x14,0x00,0x63,0x63,0x63,0x36,0x36,0x1c,0x18,0x18,0x30,0x30],  # 255 (ÿ)
]


@debugfunc
def fetch_glyph(rune):
    if isinstance(rune, bytes):
        rune = rune.decode("utf-8")

    index = ord(rune)
    if index > len(GLYPHS):
        return GLYPHS[191]  # error

    return GLYPHS[index]
