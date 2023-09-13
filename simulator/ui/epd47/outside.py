from ulogging import getLogger

logger = getLogger(__name__)

from ui import Vect, with_forecast
from .warrow import UiWArrow


class UiOutside(UiWArrow):
    @with_forecast
    def draw(self, forecast):
        # Draw wind
        weather = forecast.weather
        self.draw_wind(Vect(self.width - 230, 40), weather)

        # Type wind speed
        self.ui.text(60, f"{weather.speed:.1f}", Vect(0, -10))
        self.ui.text(25, "m/s", Vect(80, 1))

        # Type humidity
        self.ui.text(60, f"{weather.rh:.0f}", Vect(0, 45))
        self.ui.text(25, "%", Vect(80, 60))
