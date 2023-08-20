from ulogging import getLogger

logger = getLogger(__name__)

from .. import UiFrame, Vect
from display.epd import BLACK, WHITE, YELLOW
from config import vbat


class UiVBat(UiFrame):
    def draw(self, volt):
        w = self.dim.x
        h = self.dim.y
        p = min(max((volt - vbat["low_voltage"]) / (4.2 - vbat["low_voltage"]), 0), 1)
        l = int(p * (w - 1))

        if p < 0.2:
            self.canvas.fill_rect(Vect(-6, 0), Vect(w + 16, h + 18), YELLOW)
        else:
            self.canvas.fill_rect(Vect(-4, 2), Vect(w + 9, h + 14), WHITE)

        self.canvas.rect(Vect(0, 13), Vect(w + 3, h))
        self.canvas.fill_rect(Vect(-3, h // 2 + 11), Vect(3, 5))
        self.canvas.fill_rect(Vect(1 + w - l, 15), Vect(l, h - 4))
        self.ui.text_center(
            10,
            f"{volt:.2}V" if vbat["show_voltage"] else f"{p:.0%}",
            Vect(w // 2 + 2, 1),
        )

        if volt < vbat["low_voltage"]:
            self.canvas.line(Vect(13, 0), self.dim, YELLOW, w=6)
            self.canvas.line(Vect(13, 0), self.dim, BLACK, w=2)
