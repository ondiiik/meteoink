from ulogging import getLogger

logger = getLogger(__name__)

from .epd import EPD, BLACK, WHITE
import micropython
from framebuf import FrameBuffer, GS4_HMSB
from config import hw

v2d = {
    "acep": "bitmaps/acep/{}.bin",
    "bwy": "bitmaps/bwy/{}.bin",
    "epd47": "bitmaps/gs/{}.bin",
}
bmpd = v2d[hw["variant"]]


class Vect:
    @micropython.native
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @micropython.native
    def copy(self):
        return type(self)(self.x, self.y)

    @micropython.native
    def swapped(self):
        return type(self)(self.y, self.x)

    @property
    @micropython.viper
    def square(self) -> int:
        return int(self.x) * int(self.y)

    @micropython.native
    def __call__(self):
        return self.x, self.y

    @micropython.native
    def swapped(self):
        return Vect(self.y, self.x)

    @micropython.viper
    def __add__(self, v):
        return Vect(int(self.x) + int(v.x), int(self.y) + int(v.y))

    @micropython.viper
    def __sub__(self, v):
        return Vect(int(self.x) - int(v.x), int(self.y) - int(v.y))

    @micropython.viper
    def __mul__(self, v: int):
        return Vect(int(self.x) * v, int(self.y) * v)

    @micropython.viper
    def __floordiv__(self, v: int):
        return Vect(int(self.x) // v, int(self.y) // v)

    @micropython.native
    def __gt__(self, v):
        return (self.x > v.x) and (self.y > v.y)

    @micropython.native
    def __lt__(self, v):
        return (self.x < v.x) and (self.y < v.y)

    @micropython.native
    def __repr__(self):
        return f"Vect(x={self.x}, y={self.y})"


ZERO = Vect(0, 0)
ONE = Vect(1, 1)
TWO = Vect(2, 2)


class Bitmap:
    @micropython.native
    def __init__(self, bmp, no_load=False):
        self.dim = Vect(bmp[0], bmp[1])

        if no_load:
            return

        self.buf = bmp[2]

        if isinstance(self.buf, int):
            name = bmpd.format(bmp[3])
            f = open(name, "rb")
            try:
                f.seek(self.buf)
                b = f.read(bmp[0] * bmp[1] // 2)
            finally:
                f.close()

            self.buf = bytearray(b)
            bmp[2] = self.buf

        self.fb = FrameBuffer(self.buf, self.dim.x, self.dim.y, GS4_HMSB)


class Base:
    def __init__(self, t):
        self.epd = EPD()

        width, height = (
            (self.epd.height, self.epd.width)
            if t
            else (self.epd.width, self.epd.height)
        )

        self.width = width
        self.height = height
        self.dim = Vect(width, height)
        self.ofs = Vect(0, 0)
        self.buf = self.epd.fb()
        self.fb = FrameBuffer(self.buf, self.epd.width, self.epd.height, GS4_HMSB)
        self.clear()

    @micropython.native
    def clear(self):
        self.fb.fill(WHITE)

    @micropython.native
    def fill(self, c):
        self.fb.fill(c)

    @micropython.native
    def flush(self, deghost=True):
        if deghost:
            logger.info("De-ghosting ...")
            self.epd.deghost()
        logger.info("Flushing ...")
        self.epd.display_frame()

    @micropython.native
    def vtrap(self, vl1, vl2, yu1, yu2, c=BLACK):
        dx = vl2.x - vl1.x

        if dx > 0:
            kl = (vl2.y - vl1.y) / dx
            ku = (yu2 - yu1) / dx
            yl = vl1.y
            yu = yu1
            r = range(vl1.x, vl2.x + 1)
        else:
            dx = -dx
            kl = (vl1.y - vl2.y) / dx
            ku = (yu1 - yu2) / dx
            yl = vl2.y
            yu = yu2
            r = range(vl2.x, vl1.x + 1)

        for x in r:
            h = int(yl - yu)

            if h > 0:
                self.vline(Vect(x, int(yu)), int(yl - yu), c)
            else:
                self.vline(Vect(x, int(yl)), int(yu - yl), c)

            yl += kl
            yu += ku

    @micropython.native
    def vttrap(self, vl1, vl2, yu1, yu2, c=BLACK):
        dx = vl2.x - vl1.x

        if dx > 0:
            kl = (vl2.y - vl1.y) / dx
            ku = (yu2 - yu1) / dx
            yl = vl1.y
            yu = yu1
            r = range(vl1.x, vl2.x + 1)
        else:
            dx = -dx
            kl = (vl1.y - vl2.y) / dx
            ku = (yu1 - yu2) / dx
            yl = vl2.y
            yu = yu2
            r = range(vl2.x, vl1.x + 1)

        for x in r:
            h = int(yl - yu)

            if h > 0:
                self.vtline(Vect(x, int(yu)), int(yl - yu), c)
            else:
                self.vtline(Vect(x, int(yl)), int(yu - yl), c)

            yl += kl
            yu += ku


@micropython.native
def bmt(fonts, char, variant, size, color):
    fb = fonts[size][variant][variant][ord(char)]
    s = fb[2]

    if isinstance(s, int):
        name = bmpd.format(fb[3])
        with open(name, "rb") as f:
            f.seek(s)
            s = fb[2] = bytearray(f.read(fb[0] * fb[1] // 2))

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

    s = fb
    b = s[0], s[1], a
    c = fonts[size][variant].setdefault(color, dict())
    c[ord(char)] = b
    return b
