from   ui       import UiFrame, Vect, BLACK, WHITE
from   forecast import id2icon
import micropython 


class UiWeather(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
        
    @micropython.native
    def draw(self, ui, d):
        weather = ui.forecast.weather
        bitmap  = ui.bitmap(1, id2icon[weather.id])
        ui.canvas.bitmap(Vect(5, 0), bitmap)
        
        if weather.rain > 0:
            ui.text(25, '{:.1f} mm/h'.format(weather.rain), Vect(2, self.dim.y))
