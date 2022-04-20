from ulogging import getLogger
logger = getLogger(__name__)

from .base import EpdBase, V


class Epd(EpdBase):
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
                from ui.tempt import UiTempTxt
                from ui.vbat import UiVBat
                from ui.weather import UiWeather
                from ui.wind import UiWind

                weather = UiWeather(self, V(0, 0), V(self.width, 100))
                outside = UiOutside(self, V(105, 0), V(295, weather.height // 2))
                inside = UiInside(self, V(105, outside.bellow), V(295, outside.height))
                out_temp = UiOutTemp(self, V(105, 0), V(295, outside.height))
                in_temp = UiInTemp(self, V(105, out_temp.bellow), V(295, outside.height // 2 - 2))
                calendar_head = UiCalendar(self, V(0, weather.bellow), V(self.width, 32))
                icons = UiIcons(self, V(0, calendar_head.bellow + 6), V(self.width, 55))
                calendar_tail = UiCalendar(self, V(0, icons.bellow), V(self.width, self.height - icons.bellow - 30))
                graph_temp = UiTempGr(self, *calendar_tail.same)
                text_temp = UiTempTxt(self, *calendar_tail.same)
                graph_rain = UiRain(self, *calendar_tail.same)
                wind = UiWind(self, V(0, calendar_tail.bellow), V(self.width, self.height - calendar_tail.bellow))
                batt = UiVBat(self, V(284, in_temp.bellow), V(14, 10))

                calendar_head.repaint(True)
                calendar_tail.repaint(False)
                graph_temp.repaint()
                text_temp.repaint()
                graph_rain.repaint()
                wind.repaint()
                icons.repaint()
                weather.repaint()
                l = outside.repaint()
                inside.repaint(l, self.connection)
                out_temp.repaint()
                in_temp.repaint()
                batt.repaint(volt)

    def repaint_lowbat(self, volt):
        with self.Drawing('lowbat', self):
            from ui.vbat import UiVBat

            v = V(self.canvas.dim.x // 2 - 30, self.canvas.dim.y // 2)
            d = V(60, 30)
            UiVBat(self, v, d).repaint(volt)
