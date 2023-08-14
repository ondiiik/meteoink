from ulogging import getLogger

logger = getLogger(__name__)

from .. import UiFrame, V, BLUE


class UiClouds(UiFrame):
    def draw(self):
        k = self.height / 200
        m = self.height // 2
        for x1, f1, x2, f2 in self.ui.forecast_blocks():
            v1 = round(f1.clouds * k)
            v2 = round(f2.clouds * k)
            self.canvas.vttrap(V(x1, m - v1), V(x2, m - v2), m + v1, m + v2, BLUE)
            v1 = round(f1.rpb * k)
            v2 = round(f2.rpb * k)
            self.canvas.vtrap(V(x1, m - v1), V(x2, m - v2), m + v1, m + v2, BLUE)
