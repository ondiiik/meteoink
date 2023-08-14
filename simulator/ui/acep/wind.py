from ulogging import getLogger

logger = getLogger(__name__)

from .. import V, Z, UiFrame
from .warrow import UiWArrow


class UiWind(UiFrame):
    def draw(self):
        forecast = self.ui.forecast.forecast
        cnt = len(forecast) + 1
        s = V(self.height, self.height) // 2
        d = self.dim.y // 5

        for i in reversed(range(cnt - 1)):
            x = self.canvas.width * i // cnt + 5
            y = (i % 2) * d
            u = UiWArrow(self.ui, V(x, y), s)
            u.repaint(forecast[i], 4)
