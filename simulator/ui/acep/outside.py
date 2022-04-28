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
        VALWIDTH = const(110)
        spacing = self.height // 3 + 1
        valsize = V(VALWIDTH, spacing)

        # Draw wind
        weather = self.ui.forecast.weather
        u = UiWArrow(self.ui, V(VALWIDTH, 0), V(self.width - VALWIDTH, self.height))
        u.repaint(weather)

        # Type wind speed
        v = weather.speed
        y = -5
        u = UiWs(self.ui, V(0, y), valsize)
        u.repaint(v)

        # Type humidity
        y += spacing
        v = weather.rh
        u = UiRh(self.ui, V(0, y), valsize)
        u.repaint(v)

        # Type also rain intensity
        v = weather.rain
        if v > 0:
            y += spacing
            u = UiRv(self.ui, V(0, y), valsize)
            u.repaint(v)
