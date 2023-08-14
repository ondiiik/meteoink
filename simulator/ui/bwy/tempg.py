from ulogging import getLogger

logger = getLogger(__name__)

from .. import UiFrame, V, BLACK, WHITE, YELLOW
from micropython import const
from db import temp


class UiTempGr(UiFrame):
    def draw(self):
        # Pre-calculates some range values
        forecast = self.ui.forecast.forecast
        temps = [f.feel for f in forecast] + [f.temp for f in forecast]
        temp_max = max(temps)
        self.temp_min = min(temps)

        chart_space = const(30)
        chart_min = const(chart_space // 2)
        self.chart_max = self.dim.y - chart_space
        self.k_temp = (self.chart_max - chart_min) / (temp_max - self.temp_min)

        # Draw charts
        self.chart_draw(3, WHITE)
        self.chart_draw(3, YELLOW, temp.OUTDOOR_HIGH, temp.OUTDOOR_LOW)
        self.chart_draw(1, BLACK)

    def chart_draw(self, w, c, th=None, tl=None):
        for x1, f1, x2, f2 in self.ui.forecast_blocks():
            if th is None:
                v1 = V(x1, self.chart_y(f1.feel))
                v2 = V(x2, self.chart_y(f2.feel))
                self.canvas.line(v1, v2, c, w)

            if (
                (th is None)
                or (f1.feel > th)
                or (f2.feel > th)
                or (f1.feel < tl)
                or (f2.feel < tl)
            ):
                v1 = V(x1, self.chart_y(f1.temp))
                v2 = V(x2, self.chart_y(f2.temp))
                self.canvas.line(v1, v2, c, w * 2)

    def chart_y(self, temp):
        return int(self.chart_max - (temp - self.temp_min) * self.k_temp)
