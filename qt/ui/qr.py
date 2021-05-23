from ui import UiFrame, Vect, BLACK, WHITE


class UiQr(UiFrame):
    def __init__(self, ofs, dim, args):
        super().__init__(ofs, dim)
        self.txt   = args[0]
        self.lbl   = args[1]
        self.above = args[2]
        
        
    def draw(self, ui, d):
        from uqr import QRCode
        qr = QRCode()
        qr.add_data(self.txt)
        matrix = qr.get_matrix()
        
        for y in range(matrix[1]):
            for x in range(matrix[1]):
                ui.canvas.fill_rect(Vect(x * 6, y * 6),
                                    Vect(    6,     6),
                                    BLACK if matrix[0].pixel(x, y) else WHITE)
        
        l = matrix[1] * 6
        if self.above:
            ui.text_center(25, self.lbl, Vect(l // 2, -28))
        else:
            ui.text_center(25, self.lbl, Vect(l // 2, l + 10))

