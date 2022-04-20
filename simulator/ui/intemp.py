from ulogging import getLogger
logger = getLogger(__name__)

from ui import UiFrame, Vect as V, BLACK, YELLOW
from config import temp


class UiInTemp(UiFrame):
    def draw(self):
        t = self.ui.forecast.home.temp
        hl = None

        if not None == t:
            if t >= temp.indoor_high:
                hl = YELLOW

            t = '{:.1f}'.format(t)
        else:
            t = '--'

        self.ui.text(50, t, V(21, -5), BLACK, hl, 3)

        bitmap = self.ui.bitmap(1, 'in')
        self.canvas.bitmap(V(0, 30), bitmap)
