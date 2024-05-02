from ulogging import getLogger

logger = getLogger(__name__)

from ui import UiFrame, Vect, with_forecast
from display.epd import BLACK, WHITE, YELLOW
from config import temp


class UiTemp(UiFrame):
    def __init__(self, ui, ofs, dim, outside):
        super().__init__(ui, ofs, dim)
        self.outside = outside

    @with_forecast
    def draw(self, forecast):
        t = (
            (
                forecast.weather.temp
                if forecast.weather.temp_mqtt is None
                else forecast.weather.temp_mqtt
            )
            if self.outside
            else forecast.home.temp
        )
        color = WHITE

        if t is None:
            t = "--"
        else:
            if self.outside and t >= temp["outdoor_high"]:
                color = YELLOW
            t = f"{t:.1f}"

        self.ui.text(50, t, Vect(21, -5), BLACK, color)
        self.ui.text(50, "°C", Vect(self.width - 46, -5), BLACK, color)

        bitmap = self.ui.bitmap(1, "out" if self.outside else "in")
        self.canvas.bitmap(Vect(0, 30), bitmap)
