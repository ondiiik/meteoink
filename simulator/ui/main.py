from ulogging import getLogger
logger = getLogger(__name__)

from . import Ui
from display import Vect as V
from machine import reset_cause, DEEPSLEEP


class Epd(Ui):
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

            UiQr(V(0, 0), V(0, 0)).repaint(self, wifi, 'WiFi', False)
            UiQr(V(self.width - 122, self.height - 122), V(0, 0)).repaint(self, url, 'Config URL', True)
            UiUrl(V(0, self.canvas.dim.y // 2), V(self.canvas.dim.x - 132, self.canvas.dim.y // 2)).repaint(self, url)
            UiWifi(V(200, 0), V(self.canvas.dim.x - 132, self.canvas.dim.y // 2)).repaint(self, hotspot)
            UiVBat(V(self.canvas.dim.x // 2 - 10, self.canvas.dim.y // 2),  V(20, 10)).repaint(self, volt)

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


class Epd_ACEP(Epd):
    def repaint_welcome(self):
        with self.Drawing('welcome', self):
            bitmap = self.bitmap(1, 'greetings')
            self.canvas.bitmap(V(0, 0), bitmap)

    def repaint_forecast(self, volt):
        with self.Drawing('weather', self):
            if self.connection is None:
                # No forecast when there is no connection. Just draw no-wifi
                # symbol into middle of screen and leave
                bitmap = self.bitmap(1, 'nowifi')
                self.canvas.bitmap(V(177, 0), bitmap)
            else:
                # We have forecast, so lets draw it on screen. Don't draw
                # always everything as forecast is changing not so often,
                # but temperature is.
                from ui.calendar import UiCalendar
                from ui.icons import UiIcons
                from ui.inside import UiInside
                from ui.intemp import UiInTemp
                from ui.outside import UiOutside
                from ui.outtemp import UiOutTemp
                from ui.rain import UiRain
                from ui.tempg import UiTempGr
                from ui.vbat import UiVBat
                from ui.weather import UiWeather
                from ui.wind import UiWind

                weather = UiWeather(V(0, 0), V(self.width, 120))
                outside = UiOutside(V(105, 0), V(295, weather.height // 2))
                inside = UiInside(V(105, outside.bellow), V(295, outside.height))
                out_temp = UiOutTemp(V(105, 0), V(295, outside.height))
                in_temp = UiInTemp(V(105, out_temp.bellow), V(295, outside.height))

                calendar_head = UiCalendar(V(0, weather.bellow), V(self.width, 32))
                icons = UiIcons(V(0, calendar_head.bellow + 6), V(self.width, 55))
                calendar_tail = UiCalendar(V(0, icons.bellow), V(self.width, 110))
                graph_temp = UiTempGr(*calendar_tail.same)
                graph_rain = UiRain(*calendar_tail.same)
                wind = UiWind(V(0, calendar_tail.bellow), V(self.width, 30))
                batt = UiVBat(V(284, in_temp.bellow), V(14, 10))

                calendar_head.repaint(self, True)
                calendar_tail.repaint(self, False)
                graph_temp.repaint(self)
                graph_rain.repaint(self)
                wind.repaint(self)
                icons.repaint(self)
                weather.repaint(self)
                l = outside.repaint(self)
                inside.repaint(self, l, self.connection)
                out_temp.repaint(self)
                in_temp.repaint(self)
                batt.repaint(self, volt)

    def repaint_lowbat(self, volt):
        with self.Drawing('lowbat', self):
            from ui.vbat import UiVBat

            v = V(self.canvas.dim.x // 2 - 30, self.canvas.dim.y // 2)
            d = V(60, 30)
            UiVBat(v, d).repaint(self, volt)


class MeteoUi(Epd_ACEP):
    pass
