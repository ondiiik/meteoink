from ui     import UiFrame, Vect, Color
from config import temp

class UiOutTemp(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
        
    def draw(self, ui, d):
        t = ui.forecast.weather.temp
        
        if t >= temp.OUTDOOR_HIGH:
            hl = Color.YELLOW
        else:
            hl = None
            
        ui.text(50, '{:.1f}'.format(t), Vect(21, -5), Color.BLACK, hl, 3)
        
        bitmap = ui.bitmap(1, 'out')
        ui.canvas.bitmap(Vect(0, 30), bitmap)