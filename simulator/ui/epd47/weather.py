from ulogging import getLogger

logger = getLogger(__name__)

from ui import UiFrame, Vect, with_forecast
from display.epd import BLACK


class UiWeather(UiFrame):
    @with_forecast
    def draw(self, forecast):
        weather = forecast.weather
        bitmap = self.ui.bitmap(1, weather.icon)
        self.canvas.bitmap(Vect(5, 0), bitmap)

        if weather.rain > 0:
            self.ui.text_center(
                25,
                f"{weather.rain:.1f} mm/h",
                Vect(self.dim.x // 2, self.dim.y - 100),
                BLACK,
            )
