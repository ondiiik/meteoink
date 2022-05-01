from ulogging import getLogger
logger = getLogger(__name__)

from ..base import EpdBase, V, Z
from .calendar import UiCalendar
from .icons import UiIcons
from .inside import UiInside
from .intemp import UiInTemp
from .outside import UiOutside
from .outtemp import UiOutTemp
from .rain import UiRain
from .tempg import UiTempGr
from .tempt import UiTempTxt
from .weather import UiWeather
from .wind import UiWind


class Epd(EpdBase):
    def repaint_welcome(self):
        with self.Drawing('welcome', self):
            bitmap = self.bitmap(1, 'greetings')
            self.canvas.bitmap(Z, bitmap)

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
                logger.info('Drawing forecast ...')
                weather = UiWeather(self, Z, V(100, 100))
                out_temp = UiOutTemp(self, V(weather.right + 5, 0), V(160, weather.height // 2))
                in_temp = UiInTemp(self, V(weather.right + 5, out_temp.bellow), out_temp.dim)
                outside = UiOutside(self, V(out_temp.right + 5, 0), V(self.width - out_temp.right - 6, out_temp.height))
                inside = UiInside(self, V(in_temp.right + 5, outside.bellow), outside.dim)
                calendar_head = UiCalendar(self, V(0, weather.bellow), V(self.width, 32))
                icons = UiIcons(self, V(0, calendar_head.bellow + 6), V(self.width, 55))
                calendar_tail = UiCalendar(self, V(0, icons.bellow), V(self.width, self.height - icons.bellow - 30))
                graph_temp = UiTempGr(self, *calendar_tail.same)
                text_temp = UiTempTxt(self, *calendar_tail.same)
                graph_rain = UiRain(self, *calendar_tail.same)
                wind = UiWind(self, V(0, calendar_tail.bellow), V(self.width, self.height - calendar_tail.bellow))

                calendar_head.repaint(True)
                calendar_tail.repaint(False)
                graph_temp.repaint()
                text_temp.repaint(graph_temp)
                graph_rain.repaint()
                wind.repaint()
                icons.repaint()
                weather.repaint()
                outside.repaint()
                inside.repaint(self.connection, volt)
                out_temp.repaint()
                in_temp.repaint()

    def repaint_lowbat(self, volt):
        with self.Drawing('lowbat', self):
            from .vbat import UiVBat

            v = V(self.canvas.width // 2 - 30, self.canvas.height // 2)
            d = V(60, 30)
            UiVBat(self, v, d).repaint(volt)

    def repaint_config(self, volt):
        from db import spot
        from .qr import UiQr
        from .url import UiUrl
        from .vbat import UiVBat
        from .wifi import UiWifi

        with self.Drawing('hotspot', self):
            url = f'http://{self.connection.ifconfig[0]}:5555'
            wifi = f'WIFI:T:WPA;S:{spot.SSID};P:{spot.PASSWD};;'

            UiQr(self, Z, Z).repaint(wifi, 'WiFi', False)
            UiQr(self, V(self.width - 122, self.height - 122), Z).repaint(url, 'Config URL', True)
            UiUrl(self, V(0, self.canvas.height // 2), V(self.canvas.width - 132, self.canvas.height // 2)).repaint(url)
            UiWifi(self, V(200, 0), V(self.canvas.width - 132, self.canvas.height // 2)).repaint(spot)
            UiVBat(self, V(self.canvas.width // 2 - 10, self.canvas.height // 2),  V(20, 10)).repaint(volt)
