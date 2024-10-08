from ulogging import getLogger

logger = getLogger(__name__)

from .. import UiFrame, Vect
from uqr import QRCode


class UiQr(UiFrame):
    def draw(self, txt, lbl, above):
        qr = QRCode()
        qr.add_data(txt)
        matrix = qr.get_matrix()

        for y in range(matrix[1]):
            for x in range(matrix[1]):
                self.canvas.fill_rect(
                    Vect(x * 3, y * 3), Vect(3, 3), matrix[0].pixel(x, y)
                )

        l = matrix[1] * 3
        if above:
            self.ui.text_center(16, lbl, Vect(l // 2, -12))
        else:
            self.ui.text_center(16, lbl, Vect(l // 2, l))
