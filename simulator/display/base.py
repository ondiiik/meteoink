import micropython
from framebuf import FrameBuffer, GS4_HMSB
from micropython import const


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

    @micropython.native
    def copy(self):
        return type(self)(self.x, self.y)

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
    def __floordiv__(self, v: int):
        return Vect(int(self.x) // v,
                    int(self.y) // v)

    # @micropython.viper
    # def __div__(self, v: int):
    #     return Vect(int(self.x) // v,
    #                 int(self.y) // v)

    @micropython.native
    def __repr__(self):
        return f'Vect(x={self.x}, y={self.y})'


Zero = Vect(0, 0)


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
        self.buf = bytearray(((width + 1) // 2 * 2 * height) // 2)
        super().__init__(self.buf, width, height, GS4_HMSB)


class Base:
    @micropython.native
    def vtrap(self, vl1, vl2, yu1,  yu2, c=BLACK):
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
    s = fonts[size][variant][variant][ord(char)][2]
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

    s = fonts[size][variant][variant][ord(char)]
    b = s[0], s[1], a
    c = fonts[size][variant].setdefault(color, dict())
    c[ord(char)] = b
    return b
