"""
Simple script to read a bdf font and output the context in hexfont format.

For example, a BDF definition for the letter `a` could look like this (from spleen5x8.bdf):

STARTCHAR LATIN SMALL LETTER A
ENCODING 97
SWIDTH 625 0
DWIDTH 5 0
BBX 5 8 0 -1
BITMAP
00
00
60
10
70
90
70
00
ENDCHAR

in hexfont it'd look like:

0061:0000601070907000

Of course this drops a ton of useful info from the bdf definition, but it's simple enough for my use case.
"""
