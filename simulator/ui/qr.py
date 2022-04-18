from ui import UiFrame, Vect as V, BLACK, WHITE


class UiQr(UiFrame):
    def draw(self, ui, txt, lbl, above):
        from uqr import QRCode
        qr = QRCode()
        qr.add_data(txt)
        matrix = qr.get_matrix()

        for y in range(matrix[1]):
            for x in range(matrix[1]):
                ui.canvas.fill_rect(V(x * 3, y * 3),
                                    V(3, 3),
                                    BLACK if matrix[0].pixel(x, y) else WHITE)

        l = matrix[1] * 3
        if above:
            ui.text_center(10, lbl, V(l // 2, -12))
        else:
            ui.text_center(10, lbl, V(l // 2, l))
