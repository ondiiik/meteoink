from ulogging import getLogger
logger = getLogger(__name__)

from .. import UiFrame, Vect as V, BLACK, RED
from config import temp


class UiTemp(UiFrame):
    def __init__(self, ui, ofs, dim, inside):
        super().__init__(ui, ofs, dim)
        self.inside = inside

    def draw(self):
        t = self.ui.forecast.home.temp if self.inside else self.ui.forecast.weather.temp
        color = BLACK

        if t is None:
            t = '--'
        else:
            if not self.inside and t >= temp.outdoor_high:
                color = RED
            t = f'{t:.1f} °C'

        if self.inside:
            l = self.ui.text_len(50, t)
            x = self.width - l - 5
            self.ui.text(50, t, V(x, -5), color)
            bitmap = self.ui.bitmap(1, 'in')
            self.canvas.bitmap(V(x - 30, 30), bitmap)
        else:
            self.ui.text(50, t, V(5, -5), color)
