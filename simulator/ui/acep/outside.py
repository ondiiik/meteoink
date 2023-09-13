from ulogging import getLogger

logger = getLogger(__name__)

from micropython import const
from ui import Vect, UiFrame, with_forecast
from .warrow import UiWArrow
from .rh import UiRh
from .ws import UiWs
from .rv import UiRv


class UiOutside(UiFrame):
    @with_forecast
    def draw(self, forecast):
        VALWIDTH = const(100)
        OVERLAP = const(35)
        spacing = self.height // 3 + 1
        valsize = Vect(VALWIDTH, spacing)

        # Draw wind
        weather = forecast.weather
        u = UiWArrow(
            self.ui,
            Vect(VALWIDTH - OVERLAP, 0),
            Vect(self.width - VALWIDTH + OVERLAP, self.height),
        )
        u.repaint(weather)

        # Type humidity
        y = self.height - spacing
        v = weather.rh
        u = UiRh(self.ui, Vect(0, y), valsize)
        u.repaint(v)

        # Type also rain intensity (when raining)
        y -= spacing
        v = weather.rain or weather.snow
        if v > 0:
            u = UiRv(self.ui, Vect(0, y), valsize)
            u.repaint(v)

        # Type wind speed
        y -= spacing
        v = weather.speed
        u = UiWs(self.ui, Vect(0, y), valsize)
        u.repaint(v)
