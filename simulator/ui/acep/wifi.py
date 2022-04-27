from ulogging import getLogger
logger = getLogger(__name__)

from .. import UiFrame, Vect as V


class UiWifi(UiFrame):
    def draw(self, hotspot):
        self.ui.text(16, 'SSID:',        V(0, 5))
        self.ui.text(16, hotspot.ssid,   V(30, 20))
        self.ui.text(16, 'Password:',    V(0,  35))
        self.ui.text(16, hotspot.passwd, V(30, 50))
