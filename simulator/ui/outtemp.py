from ulogging import getLogger
logger = getLogger(__name__)

from ui import UiFrame, Vect as V, BLACK, YELLOW
from config import temp


class UiOutTemp(UiFrame):
    def draw(self, ui):
        t = ui.forecast.weather.temp

        if t >= temp.outdoor_high:
            hl = YELLOW
        else:
            hl = None

        ui.text(50, '{:.1f}'.format(t), V(21, -5), BLACK, hl, 3)

        bitmap = ui.bitmap(1, 'out')
        ui.canvas.bitmap(V(0, 30), bitmap)
