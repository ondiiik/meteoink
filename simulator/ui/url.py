from ulogging import getLogger
logger = getLogger(__name__)

from ui import UiFrame, Vect as V
from battery import battery


class UiUrl(UiFrame):
    def draw(self, ui, url):
        ui.canvas.hline(V(10, 0), ui.canvas.dim.x - 20)
        ui.connection.ifconfig
        ui.text(10, 'Confugurator URL:', V(15, 50))
        ui.text(10, url,                 V(45, 65))

        ui.text(10, 'VBAT {:.2f} V'.format(battery.voltage), V(0, self.dim.y - 10))
