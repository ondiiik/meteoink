from ulogging import getLogger
logger = getLogger(__name__)

from bitmap import fonts, bmp
from config import sys
from display import Vect, Bitmap, BLACK, WHITE, GREEN, BLUE, RED, YELLOW, ORANGE, ALPHA

from micropython import const

DISPLAY_REFRESH = const(0)
DISPLAY_GREETINGS = const(1)
DISPLAY_DONT_REFRESH = const(2)


class UiFrame:
    def __init__(self, ui, ofs, dim):
        self.ui = ui
        self.canvas = ui.canvas
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

    def repaint(self, *args):
        # self.canvas.rect(self.ofs, self.dim, ORANGE)
        self.canvas.ofs += self.ofs
        self.draw(*args)
        self.canvas.ofs -= self.ofs


class Ui:
    def __init__(self, canvas):
        self.canvas = canvas
        self.width = canvas.dim.x
        self.height = canvas.dim.y
        self.text_len = self.canvas.text_len
        self.text = self.canvas.text

    def bitmap(self, size, name):
        return Bitmap(bmp.bmp[name][size])

    def text_center(self, size, text, pos, color=BLACK, corona=None, border=2):
        l = self.text_len(size, text)
        pos.x -= l // 2
        return self.text(size, text, pos, color, corona, border)

    def text_right(self, size, text, pos, color=BLACK, corona=None, border=2):
        l = self.text_len(size, text)
        pos.x -= l
        return self.text(size, text, pos, color, corona, border)
