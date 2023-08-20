from ulogging import getLogger

logger = getLogger(__name__)

from .temp import UiTemp


class UiOutTemp(UiTemp):
    def __init__(self, ui, ofs, dim):
        super().__init__(ui, ofs, dim, True)
