from ulogging import getLogger
logger = getLogger(__name__)

from .. import UiFrame, V, BLACK, WHITE, YELLOW
from db import vbat


class UiVBat(UiFrame):
    def draw(self, volt):
        w = self.dim.x
        h = self.dim.y
        p = min(max((volt - vbat.LOW_VOLTAGE) / (4.2 - vbat.LOW_VOLTAGE), 0), 1)
        l = int(p * (w - 1))

        if p < 0.2:
            self.canvas.fill_rect(V(-6, 0), V(w + 16, h + 18), YELLOW)
        else:
            self.canvas.fill_rect(V(-4, 2), V(w + 9, h + 14), WHITE)

        self.canvas.rect(V(0, 13), V(w + 3, h))
        self.canvas.fill_rect(V(-3, h // 2 + 11), V(3, 5))
        self.canvas.fill_rect(V(1 + w - l, 15), V(l, h - 4))
        self.ui.text_center(10, f'{volt:.2}V' if vbat.SHOW_VOLTAGE else f'{p:.0%}', V(w // 2 + 2, 1))

        if (volt < vbat.LOW_VOLTAGE):
            self.canvas.line(V(13, 0), self.dim, YELLOW, w=6)
            self.canvas.line(V(13, 0), self.dim, BLACK,  w=2)
