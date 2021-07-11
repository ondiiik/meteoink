from   ui     import UiFrame, Vect, BLACK, WHITE, GRAY
from   config import vbat
import micropython 
        


class UiVBat(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
        
    @micropython.native
    def draw(self, ui, volt):
        w = self.dim.x
        h = self.dim.y
        p = min(max((volt - vbat.low_voltage) / (4.2 - vbat.low_voltage), 0), 1)
        l = int(p * (w - 4))
        
        ui.canvas.fill_rect(Vect(-8, -20), Vect(w + 18, h + 25), GRAY if p < 0.2 else WHITE)
        ui.canvas.rect(Vect(0, 0), Vect(w + 4, h))
        ui.canvas.rect(Vect(1, 1), Vect(w + 2, h - 2))
        ui.canvas.fill_rect(Vect(-5, h // 2 - 4), Vect(5, 8))
        ui.canvas.fill_rect(Vect(w - l, 4), Vect(l, h - 8))
        
        if vbat.show_voltage:
            ui.text_center(16, '{:.2}V'.format(volt), Vect(w // 2 + 2, -self.dim.y + 12))
        else:
            ui.text_center(16, '{:.0%}'.format(p),    Vect(w // 2 + 2, -self.dim.y + 12))
        
        if (volt < vbat.low_voltage):
            ui.canvas.line(Vect(0,0), self.dim, GRAY,  w = 6)
            ui.canvas.line(Vect(0,0), self.dim, BLACK, w = 2)

