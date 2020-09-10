from ui import UiFrame, Vect, Color

class UiInTemp(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
        
    def draw(self, ui, d):
        t  = ui.forecast.home.temp
        hl = None
        
        if not None == t:
            if t >= 27.0:
                hl = Color.YELLOW
            
            t = '{:.1f}'.format(t)
        else:
            t = '--'
            
        ui.text(50, t, Vect(21, -5), Color.BLACK, hl, 3)
        
        bitmap = ui.bitmap(1, 'in')
        ui.canvas.bitmap(Vect(0, 30), bitmap)
