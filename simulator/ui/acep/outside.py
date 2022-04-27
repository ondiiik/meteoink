from ulogging import getLogger
logger = getLogger(__name__)

from .. import Vect as V, RED, GREEN, BLUE
from .warrow import UiWArrow


class UiOutside(UiWArrow):
    def draw(self):
        # Draw wind
        weather = self.ui.forecast.weather
        self.draw_wind(V(self.width - 56, 12), weather)

        # Type wind speed
        v = weather.speed
        c = GREEN if v < 3 else BLUE if v < 12 else RED
        self.ui.text(25, f'{v:.1f}', V(0, -5), c)
        self.ui.text(10, 'm/s', V(46, 8))

        # Type humidity
        self.ui.text(25, f'{v:.0f}', V(0, 18))
        self.ui.text(10, '%', V(46, 31))

        # Type also rain intensity
        v = weather.rain
        if v > 0:
            c = GREEN if v < 1 else BLUE if v < 6 else RED
            self.ui.text(25, f'{v:.1f}', V(0, 41), c)
            self.ui.text(10, 'mm/h', V(46, 54))
