from ui import UiFrame, Vect, Color


class UiQr(UiFrame):
    __slots__ = ('txt', 'lbl', 'above')
    
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
                ui.canvas.fill_rect(Vect(x * 3, y * 3),
                                    Vect(    3,     3),
                                    Color.BLACK if matrix[0].pixel(x, y) else Color.WHITE)
        
        l = matrix[1] * 3
        if self.above:
            ui.text_center(10, self.lbl, Vect(l // 2, -12))
        else:
            ui.text_center(10, self.lbl, Vect(l // 2, l))

