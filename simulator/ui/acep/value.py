from ulogging import getLogger
logger = getLogger(__name__)

from micropython import const
from .. import UiFrame, V, BLACK

SYMDIST = const(48)
SYMDISTS = const(44)


class UiValue(UiFrame):
    def __init__(self, ui, ofs, dim, units, fmt):
        super().__init__(ui, ofs, dim)
        self.units = units
        self.fmt = fmt

    def draw(self, val):
        if val is None:
            c = BLACK
            t = '--'
        else:
            c = self.valcolor(val)
            t = self.fmt.format(val)

        self.ui.text_right(35, t, V(self.width - SYMDIST, 0), c)
        self.ui.text(16, self.units,  V(self.width - SYMDISTS, 11))

    def valcolor(self, val):
        return BLACK
