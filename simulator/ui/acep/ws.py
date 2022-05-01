from ulogging import getLogger
logger = getLogger(__name__)

from .. import RED, GREEN, BLUE
from .value import UiValue


class UiWs(UiValue):
    def __init__(self, ui, ofs, dim):
        super().__init__(ui, ofs, dim, 'm/s', '{:.1f}')

    def valcolor(self, v):
        return GREEN if v < 4 else BLUE if v < 12 else RED
