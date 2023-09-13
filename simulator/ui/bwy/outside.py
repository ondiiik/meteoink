from ulogging import getLogger

logger = getLogger(__name__)

from ui import Vect, with_forecast
from .warrow import UiWArrow


class UiOutside(UiWArrow):
    @with_forecast
    def draw(self, forecast):
        # Draw wind
        weather = forecast.weather
        self.draw_wind(Vect(self.width - 30, 0), weather)

        # Type humidity
        self.ui.text(25, f"{weather.rh:.0f}", Vect(0, 18))
        self.ui.text(10, "%", Vect(42, 31))

        # Type wind speed
        self.ui.text(25, f"{weather.speed:.1f}", Vect(0, -5))
        self.ui.text(10, "m/s", Vect(42, 8))
