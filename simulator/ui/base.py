from ulogging import getLogger, dump_exception
logger = getLogger(__name__)

from bitmap import FONTS, BMP, WIND
from display import Bitmap, BLACK, WHITE, GREEN, BLUE, RED, YELLOW, ORANGE, ALPHA
from display import Vect as V, Zero as Z


class UiFrame:
    def __init__(self, ui, ofs, dim):
        self.ui = ui
        self.canvas = ui.canvas
        self.ofs = ofs
        self.width = dim.x
        self.height = dim.y
        self.dim = dim

    @property
    def same(self):
        return self.ofs, self.dim

    @property
    def above(self):
        return self.ofs.y

    @property
    def bellow(self):
        return self.height + self.ofs.y

    @property
    def left(self):
        return self.ofs.x

    @property
    def right(self):
        return self.width + self.ofs.x

    def repaint(self, *args):
        # self.canvas.rect(self.ofs, self.dim, ORANGE)
        # self.canvas.text(16, type(self).__name__, self.ofs, ORANGE)
        self.canvas.ofs += self.ofs

        try:
            self.draw(*args)
        except Exception as e:
            dump_exception(f'Skipped {type(self).__name__} repaint', e)
            self.canvas.rect(Z, self.dim, ORANGE)
            self.canvas.line(Z, self.dim, ORANGE)
            self.canvas.line(V(0, self.dim.y), V(self.dim.x, 0), ORANGE)
            self.ui.text_center(16, str(e), self.dim // 2, color=RED, corona=YELLOW)
        finally:
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

    def wind(self, size, speed, angle):
        angle = (((angle + 187) // 15) * 15) % 360
        for level, limit in zip(range(4), (2, 4, 8, 15)):
            if speed < limit:
                return Bitmap(WIND[level][angle][size])
        return Bitmap(WIND[4][angle][size])

    def text_center(self, size, text, pos, color=BLACK, corona=None):
        l = self.text_len(size, text)
        pos.x -= l // 2
        return self.text(size, text, pos, color, corona)

    def text_right(self, size, text, pos, color=BLACK, corona=None):
        l = self.text_len(size, text)
        pos.x -= l
        return self.text(size, text, pos, color, corona)


class EpdBase(Ui):
    def __init__(self, canvas, forecast, connection, led, wdt):
        super().__init__(canvas)
        self.forecast = forecast
        self.connection = connection
        self.led = led
        self.block = 1 if forecast is None else self.canvas.width / (len(forecast.forecast) - 1)
        self.wdt = wdt

    def forecast_singles(self):
        forecast = self.forecast.forecast
        block = self.block
        x = block

        for f in forecast:
            yield int(x), f
            x += block

    def forecast_tripples(self):
        forecast = self.forecast.forecast
        block = self.block
        x = block

        for i in range(1, len(forecast) - 1):
            yield int(x), forecast[i - 1], forecast[i], forecast[i + 1]
            x += block

    def forecast_blocks(self):
        forecast = self.forecast.forecast
        block = self.block
        x1 = 0
        x2 = block

        for i1 in range(1, len(forecast)):
            yield int(x1), forecast[i1 - 1], int(x2), forecast[i1]
            x1 += block
            x2 += block

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
