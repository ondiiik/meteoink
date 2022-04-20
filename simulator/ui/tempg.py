from ulogging import getLogger
logger = getLogger(__name__)

from ui import UiFrame, Vect as V, BLACK, WHITE, YELLOW
from micropython import const
from config import temp


class UiTempGr(UiFrame):
    def draw(self, ui):
        # Pre-calculates some range values
        self.temp_min = 273.0
        forecast = ui.forecast.forecast
        cnt = len(forecast)
        self.block = ui.canvas.dim.x / cnt
        temp_max = -273.0

        for i1 in range(cnt):
            weather = forecast[i1]
            temp_max = max(weather.temp, weather.feel, temp_max)
            self.temp_min = min(weather.temp, weather.feel, self.temp_min)

        chart_space = const(30)
        chart_min = const(chart_space // 2)
        self.chart_max = self.dim.y - chart_space
        self.k_temp = (self.chart_max - chart_min) / (temp_max - self.temp_min)

        # Draw charts
        self.chart_draw(ui, 3, WHITE)
        self.chart_draw(ui, 3, YELLOW, temp.outdoor_high, temp.outdoor_low)
        self.chart_draw(ui, 1, BLACK)

    def chart_draw(self, ui, w, c, th=None, tl=None):
        forecast = ui.forecast.forecast
        cnt = len(forecast)

        for i1 in range(cnt):
            if i1 > 0:
                x1 = int(self.block * i1)
                x2 = int(x1 - self.block)
                i2 = i1 - 1
                f1 = forecast[i1].feel
                f2 = forecast[i2].feel

                if (th is None):
                    v1 = V(x1, self.chart_y(f1))
                    v2 = V(x2, self.chart_y(f2))
                    ui.canvas.line(v1, v2, c, w)

                if (th is None) or (f1 > th) or (f2 > th) or (f1 < tl) or (f2 < tl):
                    v1 = V(x1, self.chart_y(forecast[i1].temp))
                    v2 = V(x2, self.chart_y(forecast[i2].temp))
                    ui.canvas.line(v1, v2, c, w * 2)

    def chart_y(self, temp):
        return int(self.chart_max - (temp - self.temp_min) * self.k_temp)
