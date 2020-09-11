from ui          import UiFrame, Vect, Color
from micropython import const


class UiVBat(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
        
    def draw(self, ui, d):
        from vbat   import voltage
        from config import vbat
        
        w = self.dim.x
        h = self.dim.y
        v = voltage()
        p = (v - vbat.VBAT_CRITICAL) / (4.2 - vbat.VBAT_CRITICAL)
        l = int(p * w)
         
        if l < 0:
            l = 0
         
        if l < w // 3:
            ui.canvas.fill_rect(Vect(-6, -13), Vect(w + 16, h + 18), Color.YELLOW)
        else:
            ui.canvas.fill_rect(Vect(-4, -11), Vect(w + 9, h + 14), Color.WHITE)
             
        ui.canvas.rect(Vect(0, 0), Vect(w + 4, h))
        ui.canvas.fill_rect(Vect(-3, h // 2 - 2), Vect(3, 5))
        ui.canvas.fill_rect(Vect(2 + w - l, 2), Vect(l, h - 4))
        ui.text_center(10, '{:.0%}'.format(p), Vect(w // 2 + 2, -12))

