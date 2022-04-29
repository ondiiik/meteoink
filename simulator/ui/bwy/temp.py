from ulogging import getLogger
logger = getLogger(__name__)

from .. import UiFrame, V, BLACK, YELLOW, WHITE
from db import temp


class UiTemp(UiFrame):
    def __init__(self, ui, ofs, dim, outside):
        super().__init__(ui, ofs, dim)
        self.outside = outside

    def draw(self):
        t = self.ui.forecast.weather.temp if self.outside else self.ui.forecast.home.temp
        color = WHITE

        if t is None:
            t = '--'
        else:
            if self.outside and t >= temp.OUTDOOR_HIGH:
                color = YELLOW
            t = f'{t:.1f}'

        self.ui.text(50, t, V(21, -5), BLACK, color)
        self.ui.text(50, '°C', V(self.width - 46, -5), BLACK, color)

        bitmap = self.ui.bitmap(1, 'out' if self.outside else 'in')
        self.canvas.bitmap(V(0, 30), bitmap)
