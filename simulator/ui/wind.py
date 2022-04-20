from ulogging import getLogger
logger = getLogger(__name__)

from ui import Vect as V
from .warrow import UiWArrow


class UiWind(UiWArrow):
    def draw(self):
        forecast = self.ui.forecast.forecast
        cnt = len(forecast)

        for i in reversed(range(cnt)):
            x = self.canvas.dim.x * i // (cnt + 1) + 5
            y = (i % 2) * (self.dim.y // 3) + 4
            self.draw_wind(V(x, y), forecast[i], 4, True)
