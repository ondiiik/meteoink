from ulogging import getLogger

logger = getLogger(__name__)

from display.epd import RED, GREEN, BLUE
from .value import UiValue


class UiRv(UiValue):
    def __init__(self, ui, ofs, dim):
        super().__init__(ui, ofs, dim, "mm/h", "{:.1f}")

    def valcolor(self, v):
        return GREEN if v < 1 else BLUE if v < 6 else RED
