from ui import UiFrame, Vect


class UiWifi(UiFrame):
    def __init__(self, ofs, dim, hotspot):
        super().__init__(ofs, dim)
        self.hotspot = hotspot
        
        
    def draw(self, ui, d):
        ui.text(25, 'SSID:',             Vect(0,  5))
        ui.text(25, self.hotspot.ssid,   Vect(30, 5 + 30))
        ui.text(25, 'Password:',         Vect(0,  5 + 60))
        ui.text(25, self.hotspot.passwd, Vect(30, 5 + 90))

