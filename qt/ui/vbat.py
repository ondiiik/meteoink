from ui import UiFrame, Vect, Color


class UiVBat(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
        
    def draw(self, ui, volt):
        from config import vbat
        
        w = self.dim.x
        h = self.dim.y
        p = min(max((volt - vbat.VBAT_LOW) / (4.2 - vbat.VBAT_LOW), 0), 1)
        l = int(p * w)
        
        if p < 0.2:
            ui.canvas.fill_rect(Vect(-6, -13), Vect(w + 16, h + 18), Color.YELLOW)
        else:
            ui.canvas.fill_rect(Vect(-4, -11), Vect(w + 9, h + 14), Color.WHITE)
        
        ui.canvas.rect(Vect(0, 0), Vect(w + 3, h))
        ui.canvas.fill_rect(Vect(-3, h // 2 - 2), Vect(3, 5))
        ui.canvas.fill_rect(Vect(1 + w - l, 2), Vect(l, h - 4))
        
        if vbat.SHOW_VOLTAGE:
            ui.text_center(10, '{:.2}V'.format(volt), Vect(w // 2 + 2, -12))
        else:
            ui.text_center(10, '{:.0%}'.format(p), Vect(w // 2 + 2, -12))
        
        if (volt < vbat.VBAT_LOW):
            ui.canvas.line(Vect(0,0), self.dim, Color.YELLOW, w = 6)
            ui.canvas.line(Vect(0,0), self.dim, Color.BLACK,  w = 2)

