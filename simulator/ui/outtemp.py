from ulogging import getLogger
logger = getLogger(__name__)

from ui import UiFrame, Vect as V, BLACK, YELLOW
from config import temp


class UiOutTemp(UiFrame):
    def draw(self):
        t = self.ui.forecast.weather.temp

        if t >= temp.outdoor_high:
            hl = YELLOW
        else:
            hl = None

        self.ui.text(50, '{:.1f}'.format(t), V(21, -5), BLACK, hl, 3)

        bitmap = self.ui.bitmap(1, 'out')
        self.canvas.bitmap(V(0, 30), bitmap)
