# notes: gui

- sdl2 supports drop file, but not drop text
- made hexfont from the unicode font using
```
from waste.font import GLYPHS as g
hexfont = ["{:04X}".format(i) + ":" + "".join("{0:02X}".format(r) for r in hexdata) for i, hexdata in enumerate(g)]
p = pathlib.Path().home() / "hexfonts/unicode_p9-8x15.hex"
p.write_text("\n".join(hexfont), "utf-8")
```

## TODO
- implement copy
- implement paste
- implement drop images (even possible)

