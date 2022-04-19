from ulogging import getLogger
logger = getLogger(__name__)

from bitmap import fonts, bmp
from config import sys, DISPLAY_REQUIRES_FULL_REFRESH, DISPLAY_JUST_REPAINT, DISPLAY_DONT_REFRESH
from display import Vect, Bitmap, BLACK, WHITE, GREEN, BLUE, RED, YELLOW, ORANGE, ALPHA

from micropython import const


class UiFrame:
    def __init__(self, ofs, dim):
        self.ofs = ofs
        self.dim = dim

    @property
    def same(self):
        return self.ofs, self.dim

    @property
    def above(self):
        return self.ofs.y

    @property
    def bellow(self):
        return self.dim.y + self.ofs.y

    @property
    def left(self):
        return self.ofs.x

    @property
    def right(self):
        return self.dim.x + self.ofs.x

    @property
    def width(self):
        return self.dim.x

    @property
    def height(self):
        return self.dim.y

    def repaint(self, ui, *args):
        ui.canvas.ofs += self.ofs
        r = self.draw(ui, *args)
        ui.canvas.ofs -= self.ofs
        return r


class Ui:
    def __init__(self, canvas):
        self.canvas = canvas
        self.width = canvas.dim.x
        self.height = canvas.dim.y

    def bitmap(self, size, name):
        return Bitmap(bmp.bmp[name][size])

    def text_center(self, size, text, pos, color=BLACK, corona=None, border=2):
        l = self.textLength(size, text)
        pos.x -= l // 2
        return self.text(size, text, pos, color, corona, border)

    def text_right(self, size, text, pos, color=BLACK, corona=None, border=2):
        l = self.textLength(size, text)
        pos.x -= l
        return self.text(size, text, pos, color, corona, border)

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

                self.canvas.bitmap(pos, f)
                pos.x += f.dim.y + 1

        return pos

    def textLength(self, size, text):
        l = 0
        for char in text:
            if ' ' == char:
                l += int(0.3 * size) + 1
            else:
                f = Bitmap(fonts.fonts[size][ord(char)][0])
                l += f.dim.x + 1

        return l
