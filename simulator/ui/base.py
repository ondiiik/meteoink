from ulogging import getLogger
logger = getLogger(__name__)

from . import Ui
from display import Vect as V


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
