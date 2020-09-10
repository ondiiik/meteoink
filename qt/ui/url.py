from ui import UiFrame, Vect


class UiUrl(UiFrame):
    def __init__(self, ofs, dim, url):
        super().__init__(ofs, dim)
        self.url = url
        
        
    def draw(self, ui, d):
        ui.canvas.hline(Vect(10, 0), ui.canvas.dim.x - 20)
        ui.connection.ifconfig
        ui.text(10, 'Confugurator URL:', Vect(15, 50))
        ui.text(10, self.url,            Vect(45, 65))

