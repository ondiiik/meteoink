from ulogging import getLogger
logger = getLogger(__name__)

import micropython
from framebuf import FrameBuffer, GS4_HMSB

from .base import Vect, Bitmap, WHITE, BLACK, ALPHA
from .epd import EPD
from bitmap import fonts


class Canvas:
    @micropython.native
    def __init__(self):
        logger.info("Building canvas")
        self.epd = EPD()
        self.dim = Vect(self.epd.height, self.epd.width)
        self._r = self.epd.height - 1
        self.ofs = Vect(0, 0)
        logger.info("\tEPD - [ OK ]")

        self.buf = bytearray((self.epd.width * self.epd.height + 1) // 2)
        self.fb = FrameBuffer(self.buf, self.epd.width, self.epd.height, GS4_HMSB)
        self.clear()
        logger.info("\tFrame buffer - [ OK ]")

    @micropython.native
    def clear(self):
        self.fb.fill(WHITE)

    @micropython.native
    def fill(self, c):
        self.fb.fill(c)

    @micropython.native
    def flush(self, deghost=True):
        if deghost:
            logger.info('De-ghosting ...')
            self.epd.deghost(self.buf[:])
        logger.info('Flushing ...')
        self.epd.display_frame(self.buf)

    @micropython.native
    def hline(self, v, w, c=BLACK):
        v += self.ofs
        self.fb.vline(v.y, self._r - v.x - w, w, c)

    @micropython.native
    def htline(self, v, w, c=BLACK):
        v += self.ofs
        self._vtline(v.y, self._r - v.x - w, w, c)

    @micropython.native
    def _vtline(self, x, y, h, c):
        pixel = self.fb.pixel
        for y in range(y + (1 if (x + y) % 2 else 0), y + h, 2):
            pixel(x, y, c)

    @micropython.native
    def vline(self, v, h, c=BLACK):
        v += self.ofs
        self.fb.hline(v.y, self._r - v.x, h, c)

    @micropython.native
    def vtline(self, v, h, c=BLACK):
        v += self.ofs
        self._htline(v.y, self._r - v.x, h, c)

    @micropython.native
    def _htline(self, x, y, w, c):
        pixel = self.fb.pixel
        for x in range(x + (1 if (x + y) % 2 else 0), x + w, 2):
            pixel(x, y, c)

    @micropython.native
    def line(self, v1, v2, c=BLACK, w=1):
        if w < 2:
            v1 += self.ofs
            v2 += self.ofs
            self.fb.line(v1.y, self._r - v1.x, v2.y, self._r - v2.x, c)
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
        self.fb.rect(v.y, self._r - v.x - d.x, d.y, d.x, c)

    @micropython.native
    def trect(self, v, d, c=BLACK):
        v += self.ofs
        x, y = v()
        w, h = d()
        for y in range(y, y + h):
            self._vtline(y, self._r - x - w, w, c)

    @micropython.native
    def fill_rect(self, v, d, c=BLACK):
        v += self.ofs
        self.fb.fill_rect(v.y, self._r - v.x - d.x, d.y, d.x, c)

    @micropython.native
    def text(self, size, text, pos, color=BLACK, corona=None, border=2):
        if not corona is None:
            for d in (Vect(1, 0) * border,
                      Vect(0, 1) * border,
                      Vect(1, 1) * border,
                      Vect(1, -1) * border):
                self.text(size, text, pos + d, corona)
                self.text(size, text, pos - d, corona)

        for char in text:
            if ' ' == char:
                pos.x += int(0.3 * size) + 1
            else:
                try:
                    f = Bitmap(fonts.fonts[size][ord(char)][color])
                except KeyError:
                    s = fonts.fonts[size][ord(char)][0][2]
                    l = len(s)
                    a = bytearray(l)
                    for i in range(l):
                        b = s[i]
                        if b & 0x0F != 0x07:
                            b &= 0xF0
                            b |= color
                        if b & 0xF0 != 0x70:
                            b &= 0x0F
                            b |= color << 4
                        a[i] = b

                    s = fonts.fonts[size][ord(char)][0]
                    b = s[0], s[1], a
                    fonts.fonts[size][ord(char)][color] = b
                    f = Bitmap(b)

                self.bitmap(pos, f)
                pos.x += f.dim.y + 1

        return pos

    def text_len(self, size, text):
        l = 0
        for char in text:
            if ' ' == char:
                l += int(0.3 * size) + 1
            else:
                f = Bitmap(fonts.fonts[size][ord(char)][0])
                l += f.dim.y + 1

        return l

    @micropython.native
    def bitmap(self, v, bitmap):
        v += self.ofs
        self.fb.blit(bitmap.fb, v.y, self._r - v.x - bitmap.dim.y, ALPHA)
