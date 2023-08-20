from ulogging import getLogger

logger = getLogger(__name__)

from .. import UiFrame, Vect


class UiWifi(UiFrame):
    def draw(self, spot):
        self.ui.text(25, "SSID:", Vect(0, 5))
        self.ui.text(25, spot["ssid"], Vect(30, 29))
        self.ui.text(25, "Password:", Vect(0, 63))
        self.ui.text(25, spot["passwd"], Vect(30, 90))
