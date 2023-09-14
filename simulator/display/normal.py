from ulogging import getLogger

logger = getLogger(__name__)

import micropython
from micropython import const

from .base import Vect, Bitmap, bmt, Base
from .epd import ALPHA, BLACK
from bitmap import FONTS


_CORONA_SIZE = const(3)
_CORONA_SPC = const(_CORONA_SIZE + 2)
_corofs = Vect(_CORONA_SIZE, _CORONA_SIZE)


class Canvas(Base):
    rotation = 0

    @micropython.native
    def __init__(self):
        logger.info("Building canvas")
        super().__init__(False)

    @micropython.native
    def hline(self, v, w, c=BLACK):
        v += self.ofs
        self.fb.hline(v.x, v.y, w, c)

    @micropython.native
    def htline(self, v, w, c=BLACK):
        v += self.ofs
        self._htline(v.x, v.y, w, c)

    @micropython.native
    def _htline(self, x, y, w, c):
        pixel = self.fb.pixel
        for x in range(x + (1 if (x + y) % 2 else 0), x + w, 2):
            pixel(x, y, c)

    @micropython.native
    def vline(self, v, h, c=BLACK):
        v += self.ofs
        self.fb.vline(v.x, v.y, h, c)

    @micropython.native
    def vtline(self, v, h, c=BLACK):
        v += self.ofs
        self._vtline(v.x, v.y, h, c)

    @micropython.native
    def _vtline(self, x, y, h, c):
        pixel = self.fb.pixel
        for y in range(y + (1 if (x + y) % 2 else 0), y + h, 2):
            pixel(x, y, c)

    @micropython.native
    def line(self, v1, v2, c=BLACK, w=1):
        if w < 2:
            v1 += self.ofs
            v2 += self.ofs
            self.fb.line(v1.x, v1.y, v2.x, v2.y, c)
        elif w == 2:
            for a in (Vect(1, 0), Vect(0, 1), Vect(1, 1)):
                self.line(v1 + a, v2 + a, c)
        else:
            for a in (Vect(1, 0), Vect(0, 1), Vect(1, 1), Vect(1, -1)):
                for i in range(w // 2):
                    self.line(v1 + a * (i + 1), v2 + a * (i + 1), c)
                    self.line(v1 - a * (i + 1), v2 - a * (i + 1), c)

    @micropython.native
    def rect(self, v, d, c=BLACK):
        v += self.ofs
        self.fb.rect(v.x, v.y, d.x, d.y, c)

    @micropython.native
    def trect(self, v, d, c=BLACK):
        v += self.ofs
        x, y = v()
        w, h = d()
        for y in range(y, y + h):
            self._htline(x, y, w, c)

    @micropython.native
    def fill_rect(self, v, d, c=BLACK):
        v += self.ofs
        self.fb.fill_rect(v.x, v.y, d.x, d.y, c)

    @micropython.native
    def text(self, size, text, pos, color=BLACK, corona=None):
        if color is None:
            variant, color, corona = 1, corona, None
        else:
            if corona is not None:
                self.text(size, text, pos.copy(), None, corona)
            variant = 0

        pos = pos.copy() - _corofs

        for char in text:
            if " " == char:
                pos.x += int(0.3 * size) + 1
            else:
                try:
                    f = FONTS[size][variant][color][ord(char)]
                except KeyError:
                    f = bmt(FONTS, char, variant, size, color)

                f = Bitmap(f)
                self.bitmap(pos, f)
                pos.x += f.dim.x - _CORONA_SPC

        return pos

    def text_len(self, size, text):
        l = 0
        for char in text:
            if " " == char:
                l += int(0.3 * size) + 1
            else:
                f = Bitmap(FONTS[size][0][0][ord(char)], True)
                l += f.dim.x - _CORONA_SPC

        return l

    @micropython.native
    def bitmap(self, v, bitmap):
        v += self.ofs
        self.fb.blit(bitmap.fb, v.x, v.y, ALPHA)
