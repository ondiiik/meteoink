from ulogging import getLogger

logger = getLogger(__name__)

from ui import UiFrame, Vect, with_forecast
from display.epd import BLUE


class UiClouds(UiFrame):
    @with_forecast
    def draw(self, _):
        k = self.height / 200
        m = self.height // 2
        for x1, f1, x2, f2 in self.ui.forecast_blocks():
            v1 = round(f1.clouds * k)
            v2 = round(f2.clouds * k)
            self.canvas.vttrap(Vect(x1, m - v1), Vect(x2, m - v2), m + v1, m + v2, BLUE)
            v1 = round(f1.rpb * k)
            v2 = round(f2.rpb * k)
            self.canvas.vtrap(Vect(x1, m - v1), Vect(x2, m - v2), m + v1, m + v2, BLUE)
