from ulogging import getLogger

logger = getLogger(__name__)

from ui import Vect, UiFrame, with_forecast
from .warrow import UiWArrow


class UiWind(UiFrame):
    @with_forecast
    def draw(self, forecast):
        forecast = forecast.forecast
        cnt = len(forecast) + 1
        s = Vect(self.height, self.height) // 2
        d = self.dim.y // 5

        for i in reversed(range(cnt - 1)):
            x = self.canvas.width * i // cnt + 5
            y = (i % 2) * d
            u = UiWArrow(self.ui, Vect(x, y), s)
            u.repaint(forecast[i], 4)
