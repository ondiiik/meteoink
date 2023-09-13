from ulogging import getLogger

logger = getLogger(__name__)

from ui import Vect, with_forecast
from .warrow import UiWArrow


class UiWind(UiWArrow):
    @with_forecast
    def draw(self, forecast):
        forecast = forecast.forecast
        cnt = len(forecast)

        for i in reversed(range(cnt)):
            x = self.canvas.width * i // (cnt + 1) + 5
            y = (i % 2) * (self.dim.y // 3) + 4
            self.draw_wind(Vect(x, y), forecast[i], 4, True)
