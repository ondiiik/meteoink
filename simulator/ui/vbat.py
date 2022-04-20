from ulogging import getLogger
logger = getLogger(__name__)

from ui import UiFrame, Vect as V, BLACK, WHITE, YELLOW


class UiVBat(UiFrame):
    def draw(self, volt):
        from config import vbat

        w = self.dim.x
        h = self.dim.y
        p = min(max((volt - vbat.low_voltage) / (4.2 - vbat.low_voltage), 0), 1)
        l = int(p * w)

        if p < 0.2:
            self.canvas.fill_rect(V(-6, 0), V(w + 16, h + 18), YELLOW)
        else:
            self.canvas.fill_rect(V(-4, 2), V(w + 9, h + 14), WHITE)

        self.canvas.rect(V(0, 13), V(w + 3, h))
        self.canvas.fill_rect(V(-3, h // 2 + 11), V(3, 5))
        self.canvas.fill_rect(V(1 + w - l, 15), V(l, h - 4))

        if vbat.show_voltage:
            self.ui.text_center(10, '{:.2}V'.format(volt), V(w // 2 + 2, 1))
        else:
            self.ui.text_center(10, '{:.0%}'.format(p), V(w // 2 + 2, 1))

        if (volt < vbat.low_voltage):
            self.canvas.line(V(13, 0), self.dim, YELLOW, w=6)
            self.canvas.line(V(13, 0), self.dim, BLACK,  w=2)
