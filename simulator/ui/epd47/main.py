from ulogging import getLogger

logger = getLogger(__name__)

from ui.base import UiBase, Vect, ZERO
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


class MeteoUi(UiBase):
    def repaint_welcome(self):
        with self.Drawing("welcome", self):
            bitmap = self.bitmap(1, "greetings")
            self.canvas.bitmap(ZERO, bitmap)

    def repaint_forecast(self, volt):
        with self.Drawing("weather", self):
            if self.connection is None:
                # No forecast when there is no connection. Just draw no-wifi
                # symbol into middle of screen and leave
                bitmap = self.bitmap(1, "nowifi")
                self.canvas.bitmap(Vect(177, 0), bitmap)
            else:
                # We have forecast, so lets draw it on screen. Don't draw
                # always everything as forecast is changing not so often,
                # but temperature is.
                logger.info("Drawing forecast ...")
                weather = UiWeather(self, ZERO, Vect(120, 200))
                out_temp = UiOutTemp(
                    self, Vect(weather.right + 30, -12), Vect(260, weather.height // 2)
                )
                in_temp = UiInTemp(
                    self, Vect(weather.right + 30, out_temp.bellow), out_temp.dim
                )
                outside = UiOutside(
                    self,
                    Vect(out_temp.right + 110, 0),
                    Vect(self.width - out_temp.right - 110, out_temp.height),
                )
                inside = UiInside(
                    self, Vect(in_temp.right + 110, outside.bellow), outside.dim
                )
                calendar_head = UiCalendar(
                    self, Vect(0, weather.bellow + 5), Vect(self.width, 45)
                )
                icons = UiIcons(
                    self, Vect(0, calendar_head.bellow + 20), Vect(self.width, 55)
                )
                calendar_tail = UiCalendar(
                    self,
                    Vect(0, icons.bellow + 35),
                    Vect(self.width, self.height - icons.bellow - 90),
                )
                graph_temp = UiTempGr(self, *calendar_tail.same)
                text_temp = UiTempTxt(self, *calendar_tail.same)
                graph_rain = UiRain(self, *calendar_tail.same)
                wind = UiWind(
                    self,
                    Vect(0, calendar_tail.bellow + 15),
                    Vect(self.width, self.height - calendar_tail.bellow - 10),
                )

                calendar_head.repaint(True)
                calendar_tail.repaint(False)
                graph_rain.repaint()
                graph_temp.repaint()
                text_temp.repaint(graph_temp)
                wind.repaint()
                icons.repaint()
                weather.repaint()
                outside.repaint()
                inside.repaint(self.connection, volt)
                out_temp.repaint()
                in_temp.repaint()

    def repaint_lowbat(self, volt):
        with self.Drawing("lowbat", self):
            from .vbat import UiVBat

            v = Vect(self.canvas.width // 2 - 30, self.canvas.height // 2 - 15)
            d = Vect(60, 30)
            UiVBat(self, v, d).repaint(volt)

    def repaint_config(self, volt):
        from config import spot
        from .qr import UiQr
        from .url import UiUrl
        from .vbat import UiVBat
        from .wifi import UiWifi

        with self.Drawing("hotspot", self):
            url = f"http://192.168.4.1:5555"
            wifi = f"WIFI:T:WPA;S:{spot['ssid']};P:{spot['passwd']};;"

            UiQr(self, Vect(20, 25), ZERO).repaint(wifi, "WiFi", False)
            UiQr(self, Vect(self.width - 220, self.height - 220), ZERO).repaint(
                url, "Config URL", True
            )
            UiUrl(
                self,
                Vect(0, self.canvas.height // 2),
                Vect(self.canvas.width - 132, self.canvas.height // 2),
            ).repaint(url)
            UiWifi(
                self,
                Vect(270, 40),
                Vect(self.canvas.width - 132, self.canvas.height // 2),
            ).repaint(spot)
            UiVBat(
                self,
                Vect(self.canvas.width // 2 - 10, self.canvas.height // 2),
                Vect(20, 10),
            ).repaint(volt)
