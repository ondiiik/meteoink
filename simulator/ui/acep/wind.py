from ulogging import getLogger
logger = getLogger(__name__)

from .. import V, Z, UiFrame
from .warrow import UiWArrow


class UiWind(UiFrame):
    def draw(self):
        forecast = self.ui.forecast.forecast
        cnt = len(forecast)
        s = V(self.height, self.height) // 2

        for i in reversed(range(cnt)):
            x = self.canvas.dim.x * i // (cnt + 1) + 5
            y = (i % 2) * (self.dim.y // 3) + 10
            u = UiWArrow(self.ui, V(x, y), s)
            u.repaint(forecast[i], 6, True)
