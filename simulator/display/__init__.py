print('Loading module DISPLAY')
from framebuf import FrameBuffer, GS4_HMSB
from config import pins
from micropython import const
from struct import unpack
import micropython
from display import epd_acep as epaper
from machine import SPI, Pin


BLACK = const(0)
WHITE = const(1)
GREEN = const(2)
BLUE = const(3)
RED = const(4)
YELLOW = const(5)
ORANGE = const(6)
ALPHA = const(7)


class Vect:
    @micropython.native
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
        return Vect(int(self.x) + int(v.x),
                    int(self.y) + int(v.y))

    @micropython.viper
    def __sub__(self, v):
        return Vect(int(self.x) - int(v.x),
                    int(self.y) - int(v.y))

    @micropython.viper
    def __mul__(self, v: int):
        return Vect(int(self.x) * v,
                    int(self.y) * v)

    @micropython.viper
    def __div__(self, v: int):
        return Vect(int(self.x) // v,
                    int(self.y) // v)


class Bitmap:
    @micropython.native
    def __init__(self, bmp, no_load=False):
        self.dim = Vect(bmp[0], bmp[1])

        if no_load:
            return

        self.buf = bmp[2]
        self.fb = FrameBuffer(self.buf, self.dim.x, self.dim.y, GS4_HMSB)


class Frame(FrameBuffer):
    @micropython.native
    def __init__(self, width, height):
        self.buf = bytearray((width * height + 1) // 2)
        super().__init__(self.buf, width, height, GS4_HMSB)


class Canvas:
    @micropython.native
    def __init__(self):
        print("Building EPD:")

        spi = SPI(1)
        spi.init(baudrate=2000000,
                 polarity=0,
                 phase=0,
                 sck=Pin(pins.SCK),
                 mosi=Pin(pins.MOSI),
                 miso=Pin(pins.MISO))
        cs = Pin(pins.CS)
        dc = Pin(pins.DC)
        rst = Pin(pins.RST)
        busy = Pin(pins.BUSY)
        print("\tSPI - [ OK ]")

        self.epd = epaper.EPD(spi, cs, dc, rst, busy)
        self.dim = Vect(self.epd.height, self.epd.width)
        self._r = self.epd.height - 1
        self.ofs = Vect(0, 0)
        print("\tEPD - [ OK ]")

        self.buf = bytearray((self.epd.width * self.epd.height + 1) // 2)
        self.fb = FrameBuffer(self.buf, self.epd.width, self.epd.height, GS4_HMSB)
        self.clear()
        print("\tFrame buffer - [ OK ]")

    @micropython.native
    def clear(self):
        self.fb.fill(WHITE)

    @micropython.native
    def fill(self, c):
        self.fb.fill(c)

    @micropython.native
    def flush(self):
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
    def text(self, s, v, c=BLACK):
        v += self.ofs
        self.fb.text(s, v.y, self._r - v.x, c)

    @micropython.native
    def bitmap(self, v, bitmap):
        v += self.ofs
        self.fb.blit(bitmap.fb, v.y, self._r - v.x - bitmap.dim.y, ALPHA)
