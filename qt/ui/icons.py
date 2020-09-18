from ui          import UiFrame, Vect
from forecast    import id2icon
from micropython import const
import                  heap


class UiIcons(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
        
    def draw(self, ui, d):
        # Pre-calculates some range values and draw icons bar
        rows_cnt = const(2)
        forecast = ui.forecast.forecast
        cnt      = len(forecast)
        h_icons  = self.dim.y // rows_cnt
        
        for i in range(cnt):
            heap.refresh()
            xx     = ui.canvas.dim.x * i // (cnt + 1)
            bitmap = ui.bitmap(5, id2icon[forecast[i].id])
            ui.canvas.bitmap(Vect(xx, i % rows_cnt * h_icons), bitmap)
