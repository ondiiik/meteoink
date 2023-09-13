from ulogging import getLogger

logger = getLogger(__name__)

from ui import UiFrame, Vect, with_forecast
from display.epd import BLACK, BLUE, GREEN, ORANGE, RED
from micropython import const
from config import temp


class UiTempGr(UiFrame):
    @with_forecast
    def draw(self, forecast):
        stp = forecast.step
        temps = [f.feel for f in forecast.forecast] + [
            f.temp for f in forecast.forecast
        ]
        temp_max = max(temps)
        self.temp_min = min(temps)

        CHART_SPACE = const(30)
        chart_min = const(CHART_SPACE // 2)
        self.chart_max = self.height - CHART_SPACE
        self.k_temp = (self.chart_max - chart_min) / (temp_max - self.temp_min)

        def gen():
            for x1, f1, x2, f2 in self.ui.forecast_blocks():
                f = Vect(x1, self.chart_y(f1.feel)), Vect(x2, self.chart_y(f2.feel))
                t = Vect(x1, self.chart_y(f1.temp)), Vect(x2, self.chart_y(f2.temp))
                rl = f1.srt + stp
                rh = f1.sst + stp
                dl = (rl < f1.dt < rh) or (rl < f1.dt < rh)

                v = max(f1.feel, f2.feel, f1.temp, f2.temp)
                if v > temp["outdoor_high"]:
                    d = self.canvas.vtrap
                    c = ORANGE if dl else RED
                else:
                    v = min(f1.feel, f2.feel, f1.temp, f2.temp)
                    if v < temp["outdoor_low"]:
                        d = self.canvas.vttrap if dl else self.canvas.vtrap
                        c = BLUE
                    else:
                        d = self.canvas.vttrap if dl else self.canvas.vtrap
                        c = GREEN

                yield d, c, t, f

        gen = list(gen())

        for d, c, t, f in gen:
            d(t[0], t[1], self.height, self.height, c)
            self.canvas.line(t[0], t[1], c, 2)

        for d, c, t, f in gen:
            self.canvas.line(f[0], f[1], BLACK, 2)

    def chart_y(self, temp):
        return int(self.chart_max - (temp - self.temp_min) * self.k_temp)
