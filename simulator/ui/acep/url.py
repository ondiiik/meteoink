from ulogging import getLogger

logger = getLogger(__name__)

from .. import UiFrame, V
from battery import battery


class UiUrl(UiFrame):
    def draw(self, url):
        self.canvas.hline(V(10, 0), self.canvas.width - 20)
        self.ui.connection.ifconfig
        self.ui.text(16, "Confugurator URL:", V(15, 50))
        self.ui.text(16, url, V(45, 65))
