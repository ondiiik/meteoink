from ulogging import getLogger
logger = getLogger(__name__)

from micropython import const
from .. import Vect as V, RED, GREEN, BLUE
from .warrow import UiWArrow


class UiOutside(UiWArrow):
    def draw(self):
        SPACING = const(28)
        LOWERING = const(13)
        SYMDIST = const(52)
        SYMDISTS = const(56)

        # Draw wind
        weather = self.ui.forecast.weather
        self.draw_wind(V(self.width - 56, 12), weather)

        # Type wind speed
        v = weather.speed
        y = -5

        c = GREEN if v < 3 else BLUE if v < 12 else RED
        self.ui.text_right(35, f'{v:.1f}', V(SYMDIST, y), c)
        self.ui.text(16, 'm/s', V(SYMDISTS, y + LOWERING))

        # Type humidity
        y += SPACING
        self.ui.text_right(35, f'{v:.0f}', V(SYMDIST, y))
        self.ui.text(16, '%', V(SYMDISTS, y + LOWERING))

        # Type also rain intensity
        v = weather.rain
        if v > 0:
            c = GREEN if v < 1 else BLUE if v < 6 else RED
            y += SPACING
            self.ui.text_right(35, f'{v:.1f}', V(SYMDIST, y), c)
            self.ui.text(16, 'mm/h', V(SYMDISTS, y + LOWERING))
