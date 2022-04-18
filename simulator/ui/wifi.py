from ui import UiFrame, Vect as V


class UiWifi(UiFrame):
    def draw(self, ui, hotspot):
        ui.text(10, 'SSID:',        V(0, 5))
        ui.text(10, hotspot.ssid,   V(30, 20))
        ui.text(10, 'Password:',    V(0,  35))
        ui.text(10, hotspot.passwd, V(30, 50))
