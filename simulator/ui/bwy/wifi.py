from ulogging import getLogger

logger = getLogger(__name__)

from .. import UiFrame, Vect


class UiWifi(UiFrame):
    def draw(self, spot):
        self.ui.text(10, "SSID:", Vect(0, 5))
        self.ui.text(10, spot["ssid"], Vect(30, 20))
        self.ui.text(10, "Password:", Vect(0, 35))
        self.ui.text(10, spot["passwd"], Vect(30, 50))
