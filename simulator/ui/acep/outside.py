from ulogging import getLogger
logger = getLogger(__name__)

from micropython import const
from .. import V, UiFrame
from .warrow import UiWArrow
from .rh import UiRh
from .ws import UiWs
from .rv import UiRv


class UiOutside(UiFrame):
    def draw(self):
        VALWIDTH = const(100)
        OVERLAP = const(30)
        spacing = self.height // 3 + 1
        valsize = V(VALWIDTH, spacing)

        # Draw wind
        weather = self.ui.forecast.weather
        u = UiWArrow(self.ui, V(VALWIDTH - OVERLAP, 0), V(self.width - VALWIDTH + OVERLAP, self.height))
        u.repaint(weather)

        # Type humidity
        y = self.height - spacing
        v = weather.rh
        u = UiRh(self.ui, V(0, y), valsize)
        u.repaint(v)

        # Type also rain intensity (when raining)
        y -= spacing
        v = weather.rain or weather.snow
        if v > 0:
            u = UiRv(self.ui, V(0, y), valsize)
            u.repaint(v)

        # Type wind speed
        y -= spacing
        v = weather.speed
        u = UiWs(self.ui, V(0, y), valsize)
        u.repaint(v)
