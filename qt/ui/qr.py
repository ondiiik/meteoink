from ui import UiFrame, Vect, Color


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
        
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                ui.canvas.fill_rect(Vect(x * 3, y * 3),
                                    Vect(    3,     3),
                                    Color.BLACK if matrix[y][x] else Color.WHITE)
        
        l = len(matrix) * 3
        if self.above:
            ui.text_center(10, self.lbl, Vect(l // 2, -12))
        else:
            ui.text_center(10, self.lbl, Vect(l // 2, l))

