from ulogging import getLogger
logger = getLogger(__name__)

from ui import Vect as V
from .warrow import UiWArrow


class UiOutside(UiWArrow):
    def draw(self):
        # Draw wind
        weather = self.ui.forecast.weather
        self.draw_wind(V(260, 0), weather)

        # Type celsius symbol
        self.ui.text(50, '°C', V(111, -5))

        # Type humidity
        t = '{:.0f}'.format(weather.rh)
        self.ui.text(25, t, V(175, 18))
        l = self.ui.textLength(25, t) + 6
        self.ui.text(10, '%',  V(175 + l, 31))

        # Type wind speed
        self.ui.text(25, '{:.1f}'.format(weather.speed), V(175, -5))
        self.ui.text(10, 'm/s', V(175 + l, 8))

        return l
