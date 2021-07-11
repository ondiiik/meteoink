from   ui      import UiFrame, Vect, BLACK
from   battery import battery
import micropython


class UiUrl(UiFrame):
    def __init__(self, ofs, dim, url):
        super().__init__(ofs, dim)
        self.url = url
        
        
    @micropython.native
    def draw(self, ui, d):
        ui.canvas.fill_rect(Vect(10, 0), Vect(ui.canvas.dim.x - 20, 3), BLACK)
        ui.text(25, 'Confugurator URL:', Vect(15, 50))
        ui.text(25, self.url,            Vect(45, 50 + 30))
        
        ui.text(25, 'VBAT {:.2f} V'.format(battery.voltage), Vect(0, self.dim.y - 30))

