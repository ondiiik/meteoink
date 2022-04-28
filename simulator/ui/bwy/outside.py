from ulogging import getLogger
logger = getLogger(__name__)

from .. import V
from .warrow import UiWArrow


class UiOutside(UiWArrow):
    def draw(self):
        # Draw wind
        weather = self.ui.forecast.weather
        self.draw_wind(V(self.width - 30, 0), weather)

        # Type humidity
        self.ui.text(25, f'{weather.rh:.0f}', V(0, 18))
        self.ui.text(10, '%', V(42, 31))

        # Type wind speed
        self.ui.text(25, f'{weather.speed:.1f}', V(0, -5))
        self.ui.text(10, 'm/s', V(42, 8))
