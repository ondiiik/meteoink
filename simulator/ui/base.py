from ulogging import getLogger
logger = getLogger(__name__)


from bitmap import FONTS, BMP
from display import Bitmap, BLACK, WHITE, GREEN, BLUE, RED, YELLOW, ORANGE, ALPHA
from display import Vect as V, Zero as Z


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
        # self.canvas.text(16, type(self).__name__, self.ofs, ORANGE)
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
        return Bitmap(BMP[name][size])

    def text_center(self, size, text, pos, color=BLACK, corona=None):
        l = self.text_len(size, text)
        pos.x -= l // 2
        return self.text(size, text, pos, color, corona)

    def text_right(self, size, text, pos, color=BLACK, corona=None):
        l = self.text_len(size, text)
        pos.x -= l
        return self.text(size, text, pos, color, corona)


class EpdBase(Ui):
    def __init__(self, canvas, forecast, connection, led):
        super().__init__(canvas)
        self.forecast = forecast
        self.connection = connection
        self.led = led

    class Drawing:
        def __init__(self, name, epd):
            self.name = name
            self.epd = epd

        def __enter__(self):
            logger.info(f'Drawing {self.name} ...')
            self.epd.led.mode(self.epd.led.DRAWING)
            self.epd.canvas.clear()

        def __exit__(self, *args):
            logger.info(f'Flushing {self.name} ...')
            self.epd.led.mode(self.epd.led.FLUSHING)
            self.epd.canvas.flush()
