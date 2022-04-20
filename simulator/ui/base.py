from ulogging import getLogger
logger = getLogger(__name__)

from . import Ui
from display import Vect as V
from machine import reset_cause, DEEPSLEEP


class EpdBase(Ui):
    def __init__(self, canvas, forecast, connection, led):
        super().__init__(canvas)
        self.forecast = forecast
        self.connection = connection
        self.led = led

    def repaint_config(self, volt):
        from config.spot import hotspot
        from ui.qr import UiQr
        from ui.url import UiUrl
        from ui.vbat import UiVBat
        from ui.wifi import UiWifi

        with self.Drawing('hotspot', self):
            url = f'http://{self.connection.ifconfig[0]}:5555'
            wifi = f'WIFI:T:WPA;S:{hotspot.ssid};P:{hotspot.passwd};;'

            UiQr(self, V(0, 0), V(0, 0)).repaint(wifi, 'WiFi', False)
            UiQr(self, V(self.width - 122, self.height - 122), V(0, 0)).repaint(url, 'Config URL', True)
            UiUrl(self, V(0, self.canvas.dim.y // 2), V(self.canvas.dim.x - 132, self.canvas.dim.y // 2)).repaint(url)
            UiWifi(self, V(200, 0), V(self.canvas.dim.x - 132, self.canvas.dim.y // 2)).repaint(hotspot)
            UiVBat(self, V(self.canvas.dim.x // 2 - 10, self.canvas.dim.y // 2),  V(20, 10)).repaint(volt)

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
            self.epd.canvas.flush(reset_cause() != DEEPSLEEP)
