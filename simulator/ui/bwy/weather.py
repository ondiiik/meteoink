from ulogging import getLogger

logger = getLogger(__name__)

from .. import UiFrame, Vect
from display.epd import BLACK, WHITE


class UiWeather(UiFrame):
    def draw(self):
        weather = self.ui.forecast.weather
        bitmap = self.ui.bitmap(1, weather.icon)
        self.canvas.bitmap(Vect(5, 0), bitmap)

        if weather.rain > 0:
            self.ui.text(
                10, f"{weather.rain:.1f} mm/h", Vect(2, self.dim.y - 14), BLACK, WHITE
            )
