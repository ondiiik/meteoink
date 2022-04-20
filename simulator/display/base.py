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
