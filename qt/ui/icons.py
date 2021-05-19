from ui          import UiFrame, Vect
from forecast    import id2icon
from micropython import const


_ICONS_ROWS = const(2)


class UiIcons(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
        
    def draw(self, ui, d):
        # Pre-calculates some range values and draw icons bar
        forecast = ui.forecast.forecast
        cnt      = len(forecast)
        h_icons  = self.dim.y // _ICONS_ROWS
        icon     = {}
        
        for i in range(cnt):
            xx = ui.canvas.dim.x * i // (cnt + 1)
            id = forecast[i].id
            
            try:
                bitmap = icon[id]
            except KeyError:
                bitmap   = ui.bitmap(2, id2icon[id])
                icon[id] = bitmap
            
            ui.canvas.bitmap(Vect(xx, i % _ICONS_ROWS * h_icons), bitmap)
