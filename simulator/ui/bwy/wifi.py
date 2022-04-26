from ulogging import getLogger
logger = getLogger(__name__)

from .. import UiFrame, Vect as V


class UiWifi(UiFrame):
    def draw(self, hotspot):
        self.ui.text(10, 'SSID:',        V(0, 5))
        self.ui.text(10, hotspot.ssid,   V(30, 20))
        self.ui.text(10, 'Password:',    V(0,  35))
        self.ui.text(10, hotspot.passwd, V(30, 50))
