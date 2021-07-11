from   ui          import UiFrame, Vect
from   forecast    import id2icon
from   micropython import const
import micropython 


_ICONS_ROWS = const(2)


class UiIcons(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
        
    @micropython.native
    def draw(self, ui, d):
        # Pre-calculates some range values and draw icons bar
        forecast = ui.forecast.forecast
        cnt      = ui.forecast.cnt
        daily    = ui.forecast.daily
        h_icons  = 1 if daily else self.dim.y // _ICONS_ROWS
        icon     = {}
        inc      = 0   if daily else 1
        bsize    = 1   if daily else 2
        bvofs    = 72  if daily else 0
        bhofs    = -28 if daily else 0
        
        for i in range(cnt):
            xx = ui.canvas.dim.x * i // (cnt + inc)
            id = forecast[i].id
            
            try:
                bitmap = icon[id]
            except KeyError:
                bitmap   = ui.bitmap(bsize, id2icon[id])
                icon[id] = bitmap
            
            ui.canvas.bitmap(Vect(xx + bvofs, i % _ICONS_ROWS * h_icons + bhofs), bitmap)
