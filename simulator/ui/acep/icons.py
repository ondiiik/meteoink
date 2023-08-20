from ulogging import getLogger

logger = getLogger(__name__)

from .. import UiFrame, Vect
from micropython import const


class UiIcons(UiFrame):
    def draw(self):
        # Pre-calculates some range values and draw icons bar
        rows_cnt = const(2)
        forecast = self.ui.forecast.forecast
        cnt = len(forecast)
        h_icons = self.dim.y // rows_cnt
        icon = {}

        for i in range(cnt):
            xx = self.canvas.width * i // (cnt + 1)
            fid = forecast[i].icon

            try:
                bitmap = icon[fid]
            except KeyError:
                bitmap = self.ui.bitmap(4, fid)
                icon[fid] = bitmap

            self.canvas.bitmap(Vect(xx, i % rows_cnt * h_icons), bitmap)
