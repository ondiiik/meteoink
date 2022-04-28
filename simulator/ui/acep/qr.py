from ulogging import getLogger
logger = getLogger(__name__)

from .. import UiFrame, V
from uqr import QRCode
from micropython import const


_PIX_SIZE = const(4)
_pix_dim = V(_PIX_SIZE, _PIX_SIZE)


class UiQr(UiFrame):
    def draw(self, txt, lbl, above):
        qr = QRCode()
        qr.add_data(txt)
        matrix = qr.get_matrix()

        for y in range(matrix[1]):
            for x in range(matrix[1]):
                self.canvas.fill_rect(V(x * _PIX_SIZE, y * _PIX_SIZE), _pix_dim, matrix[0].pixel(x, y))

        l = matrix[1] * _PIX_SIZE
        if above:
            self.ui.text_center(16, lbl, V(l // 2, -12))
        else:
            self.ui.text_center(16, lbl, V(l // 2, l))
