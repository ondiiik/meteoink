from ui      import UiFrame, Vect
from battery import battery


class UiUrl(UiFrame):
    def __init__(self, ofs, dim, url):
        super().__init__(ofs, dim)
        self.url = url
        
        
    def draw(self, ui, d):
        ui.canvas.hline(Vect(10, 0), ui.canvas.dim.x - 20)
        ui.connection.ifconfig
        ui.text(10, 'Confugurator URL:', Vect(15, 50))
        ui.text(10, self.url,            Vect(45, 65))
        
        ui.text(10, 'VBAT {:.2f} V'.format(battery.voltage), Vect(0, self.dim.y - 10))

