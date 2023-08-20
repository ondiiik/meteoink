from ulogging import getLogger

logger = getLogger(__name__)

from micropython import const
from config import vbat
from ui import UiFrame, Vect
from display.epd import ORANGE, RED, GREEN, YELLOW


class UiVBat(UiFrame):
    def draw(self, volt):

        YOFFS = const(24)

        w = self.dim.x - 4
        h = self.dim.y - 22
        p = min(max((volt - vbat["low_voltage"]) / (4.2 - vbat["low_voltage"]), 0), 1)
        l = int(p * (w - 1))

        color = RED if p < 0.2 else ORANGE if p < 0.4 else YELLOW if p < 0.5 else GREEN
        self.canvas.rect(Vect(0, YOFFS - 2), Vect(w + 3, h))
        self.canvas.fill_rect(Vect(-3, h // 2 + YOFFS - 4), Vect(3, 5))
        self.canvas.fill_rect(Vect(1 + w - l, YOFFS), Vect(l, h - 4), color)
        self.ui.text_center(
            16,
            f"{volt:.2}V" if vbat["show_voltage"] else f"{p:.0%}",
            Vect(w // 2 + 2, 0),
        )
