from ulogging import getLogger

logger = getLogger(__name__)

from ui import UiFrame, Vect
from display.epd import BLACK, WHITE


class UiTemp(UiFrame):
    def __init__(self, ui, ofs, dim, outside):
        super().__init__(ui, ofs, dim)
        self.outside = outside

    def draw(self):
        t = (
            self.ui.forecast.weather.temp
            if self.outside
            else self.ui.forecast.home.temp
        )

        if t is None:
            t = "--"
        else:
            t = f"{t:.1f}"

        self.ui.text(100, t, Vect(31, -5), BLACK, WHITE)
        self.ui.text(100, "°C", Vect(self.width - 46, -5), BLACK, WHITE)

        bitmap = self.ui.bitmap(1, "out" if self.outside else "in")
        self.canvas.bitmap(Vect(-20, 30), bitmap)
