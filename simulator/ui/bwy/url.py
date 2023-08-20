from ulogging import getLogger

logger = getLogger(__name__)

from .. import UiFrame, Vect
from battery import battery


class UiUrl(UiFrame):
    def draw(self, url):
        self.canvas.hline(Vect(10, 0), self.canvas.width - 20)
        self.ui.connection.ifconfig
        self.ui.text(10, "Confugurator URL:", Vect(15, 50))
        self.ui.text(10, url, Vect(45, 65))
