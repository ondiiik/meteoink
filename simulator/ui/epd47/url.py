from ulogging import getLogger

logger = getLogger(__name__)

from ui import UiFrame, Vect


class UiUrl(UiFrame):
    def draw(self, url):
        self.canvas.hline(Vect(10, 0), self.canvas.width - 20)
        self.ui.text(25, "Confugurator URL:", Vect(15, 50))
        self.ui.text(25, url, Vect(45, 80))
