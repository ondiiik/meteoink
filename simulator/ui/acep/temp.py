from ulogging import getLogger

logger = getLogger(__name__)

from .. import UiFrame, Vect
from display.epd import BLACK, RED
from config import temp


class UiTemp(UiFrame):
    def __init__(self, ui, ofs, dim, inside):
        super().__init__(ui, ofs, dim)
        self.inside = inside

    def draw(self):
        t = self.ui.forecast.home.temp if self.inside else self.ui.forecast.weather.temp
        color = BLACK

        if t is None:
            t = "--"
        else:
            if not self.inside and t >= temp["outdoor_high"]:
                color = RED
            t = f"{t:.1f}"

        s = "°C"
        if self.inside:
            l = self.ui.text_len(35, s)
            x = self.width - l - 5
            self.ui.text(35, s, Vect(x, 8))

            l = self.ui.text_len(60, t)
            x -= l + 5
            self.ui.text(60, t, Vect(x, -5), color)

            bitmap = self.ui.bitmap(1, "in")
            self.canvas.bitmap(Vect(x - 25, self.height - 24), bitmap)
        else:
            p = self.ui.text(60, t, Vect(5, -5), color)
            self.ui.text(35, s, p + Vect(6, 16))
