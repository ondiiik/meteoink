from ulogging import getLogger
logger = getLogger(__name__)

from ui import UiFrame, Vect as V
from uqr import QRCode


class UiQr(UiFrame):
    def draw(self, txt, lbl, above):
        qr = QRCode()
        qr.add_data(txt)
        matrix = qr.get_matrix()

        for y in range(matrix[1]):
            for x in range(matrix[1]):
                self.canvas.fill_rect(V(x * 3, y * 3), V(3, 3), matrix[0].pixel(x, y))

        l = matrix[1] * 3
        if above:
            self.ui.text_center(10, lbl, V(l // 2, -12))
        else:
            self.ui.text_center(10, lbl, V(l // 2, l))
