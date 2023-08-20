from ulogging import getLogger

logger = getLogger(__name__)
from config import behavior
from ..base import UiBase, Vect, ZERO
from .calendar import UiCalendar
from .clouds import UiClouds
from .icons import UiIcons
from .inside import UiInside
from .intemp import UiInTemp
from .outside import UiOutside
from .outtemp import UiOutTemp
from .radar import UiRadar
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
        if self.connection is not None:
            with self.Drawing("weather", self):
                # We have forecast, so lets draw it on screen. Don't draw
                # always everything as forecast is changing not so often,
                # but temperature is.
                logger.info("Drawing forecast ...")

                if behavior["show_radar"]:
                    weather = UiRadar(self, ZERO, Vect(240, 180))
                    outside = UiOutside(self, Vect(weather.right, 0), Vect(210, 120))
                    inside = UiInside(
                        self,
                        Vect(weather.right, weather.bellow - 80),
                        Vect(self.width - weather.right, 80),
                    )
                    out_temp = UiOutTemp(
                        self,
                        Vect(weather.left, weather.bellow),
                        Vect(weather.width, 60),
                    )
                else:
                    weather = UiWeather(self, ZERO, Vect(130, 120))
                    outside = UiOutside(
                        self, Vect(weather.right, 0), Vect(210, weather.height)
                    )
                    inside = UiInside(
                        self,
                        Vect(outside.right, 0),
                        Vect(self.width - outside.right, weather.height),
                    )
                    out_temp = UiOutTemp(
                        self,
                        Vect(weather.left, weather.bellow),
                        Vect(self.width // 2, 60),
                    )

                in_temp = UiInTemp(
                    self,
                    Vect(out_temp.right, out_temp.above),
                    Vect(self.width - out_temp.width, out_temp.height),
                )
                calendar_head = UiCalendar(
                    self, Vect(0, in_temp.bellow), Vect(self.width, 46)
                )
                icons = UiIcons(
                    self, Vect(0, calendar_head.bellow + 12), Vect(self.width, 72)
                )
                calendar_tail = UiCalendar(
                    self,
                    Vect(0, icons.bellow + 12),
                    Vect(self.width, self.height - icons.bellow - 60),
                )
                clouds = UiClouds(
                    self, Vect(0, calendar_tail.above + 8), Vect(self.width, 40)
                )
                graph_temp = UiTempGr(
                    self,
                    Vect(0, clouds.bellow + 12),
                    Vect(self.width, calendar_tail.height - clouds.height - 24),
                )
                text_temp = UiTempTxt(self, *graph_temp.same)
                graph_rain = UiRain(self, *graph_temp.same)
                wind = UiWind(
                    self,
                    Vect(0, calendar_tail.bellow + 16),
                    Vect(self.width, self.height - calendar_tail.bellow - 16),
                )

                calendar_head.repaint(True)
                calendar_tail.repaint(False)
                graph_temp.repaint()
                text_temp.repaint(graph_temp)
                wind.repaint()
                graph_rain.repaint()
                clouds.repaint()
                icons.repaint()
                weather.repaint(self.connection, self.wdt)
                outside.repaint()
                inside.repaint(self.connection, volt, behavior["show_radar"])
                out_temp.repaint()
                in_temp.repaint()

    def repaint_lowbat(self, volt):
        with self.Drawing("lowbat", self):
            from .vbat import UiVBat

            v = Vect(self.canvas.width // 2 - 30, self.canvas.height // 2)
            d = Vect(60, 30)
            UiVBat(self, v, d).repaint(volt)

    def repaint_config(self, volt):
        from config import spot
        from .qr import UiQr
        from .url import UiUrl
        from .vbat import UiVBat
        from .wifi import UiWifi

        with self.Drawing("hotspot", self):
            url = f"http://{self.connection.ifconfig[0]}:5555"
            wifi = f"WIFI:T:WPA;S:{spot['ssid']};P:{spot['passwd']};;"

            logger.info(f"Listening on {url}")

            UiQr(self, ZERO, ZERO).repaint(wifi, "WiFi", False)
            UiQr(self, Vect(self.width - 140, self.height - 140), ZERO).repaint(
                url, "Config URL", True
            )
            UiUrl(
                self,
                Vect(0, self.canvas.height // 2),
                Vect(self.canvas.width - 132, self.canvas.height // 2),
            ).repaint(url)
            UiWifi(
                self,
                Vect(200, 0),
                Vect(self.canvas.width - 132, self.canvas.height // 2),
            ).repaint(spot)
            UiVBat(
                self,
                Vect(self.canvas.width // 2 - 10, self.canvas.height // 2),
                Vect(20, 32),
            ).repaint(volt)
