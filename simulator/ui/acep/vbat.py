from ulogging import getLogger
logger = getLogger(__name__)

from .. import UiFrame, Vect as V, BLACK, ORANGE, RED, GREEN, YELLOW


class UiVBat(UiFrame):
    def draw(self, volt):
        from config import vbat

        w = self.dim.x
        h = self.dim.y
        p = min(max((volt - vbat.low_voltage) / (4.2 - vbat.low_voltage), 0), 1)
        l = int(p * (w - 1))

        color = RED if p < 0.2 else ORANGE if p < 0.4 else YELLOW if p < 0.5 else GREEN
        self.canvas.rect(V(0, 13), V(w + 3, h))
        self.canvas.fill_rect(V(-3, h // 2 + 11), V(3, 5))
        self.canvas.fill_rect(V(1 + w - l, 15), V(l, h - 4), color)
        self.ui.text_center(10, f'{volt:.2}V' if vbat.show_voltage else f'{p:.0%}', V(w // 2 + 2, 1))

        if (volt < vbat.low_voltage):
            self.canvas.line(V(13, 0), self.dim, YELLOW, w=6)
            self.canvas.line(V(13, 0), self.dim, BLACK,  w=2)
