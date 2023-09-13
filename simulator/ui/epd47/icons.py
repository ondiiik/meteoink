from ulogging import getLogger

logger = getLogger(__name__)

from ui import UiFrame, Vect, with_forecast
from micropython import const


class UiIcons(UiFrame):
    @with_forecast
    def draw(self, forecast):
        # Pre-calculates some range values and draw icons bar
        rows_cnt = const(2)
        forecast = forecast.forecast
        cnt = len(forecast)
        h_icons = self.dim.y // rows_cnt
        icon = {}

        for i in range(cnt):
            xx = self.canvas.width * i // (cnt + 1)
            fid = forecast[i].icon

            try:
                bitmap = icon[fid]
            except KeyError:
                bitmap = self.ui.bitmap(2, fid)
                icon[fid] = bitmap

            self.canvas.bitmap(Vect(xx, i % rows_cnt * h_icons), bitmap)
