from ulogging import getLogger
logger = getLogger(__name__)

from .. import UiFrame, Vect as V
from battery import battery


class UiUrl(UiFrame):
    def draw(self, url):
        self.canvas.hline(V(10, 0), self.canvas.dim.x - 20)
        self.ui.connection.ifconfig
        self.ui.text(10, 'Confugurator URL:', V(15, 50))
        self.ui.text(10, url,                 V(45, 65))

        self.ui.text(10, 'VBAT {:.2f} V'.format(battery.voltage), V(0, self.dim.y - 10))
