from ulogging import getLogger
logger = getLogger(__name__)

from .. import RED, GREEN, BLUE
from .value import UiValue


class UiRh(UiValue):
    def __init__(self, ui, ofs, dim):
        super().__init__(ui, ofs, dim, '%RH', '{:.0f}')

    def valcolor(self, v):
        return RED if v < 40 else GREEN if v < 60 else BLUE
