from ui import UiFrame, Vect


class UiWifi(UiFrame):
    def __init__(self, ofs, dim, hotspot):
        super().__init__(ofs, dim)
        self.hotspot = hotspot
        
        
    def draw(self, ui, d):
        ui.text(10, 'SSID:',             Vect(0, 5))
        ui.text(10, self.hotspot.ssid,   Vect(30, 20))
        ui.text(10, 'Password:',         Vect(0,  35))
        ui.text(10, self.hotspot.passwd, Vect(30, 50))

