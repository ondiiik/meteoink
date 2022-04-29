from ulogging import getLogger
logger = getLogger(__name__)

from .. import UiFrame, V


class UiWifi(UiFrame):
    def draw(self, spot):
        self.ui.text(10, 'SSID:',     V(0, 5))
        self.ui.text(10, spot.SSID,   V(30, 20))
        self.ui.text(10, 'Password:', V(0,  35))
        self.ui.text(10, spot.PASSWD, V(30, 50))
