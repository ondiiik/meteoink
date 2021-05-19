from ui          import UiFrame, Vect
from config      import location
from micropython import const


_INSIDE_OFS_A  = const(70)
_INSIDE_OFS_80 = const(-10)
_INSIDE_OFS_B  = const(_INSIDE_OFS_A  + 10)
_INSIDE_OFS_50 = const(_INSIDE_OFS_80 + 20)


class UiInside(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
    def draw(self, ui, args):
        connection = args[0]
        
        # Type humidity
        t = '--' if None == ui.forecast.home.rh else '{:.0f}'.format(ui.forecast.home.rh)
        ui.text_right(80, t,   Vect(_INSIDE_OFS_A, _INSIDE_OFS_80))
        ui.text(      50, '% RH', Vect(_INSIDE_OFS_B, _INSIDE_OFS_50))
        
        
        # Type weather details
        # ui.text_right(16, ui.forecast.descr, Vect(self.dim.x, 15))
        # ui.text_right(10, location[connection.config.location].name, Vect(self.dim.x, 35))
        # dt = ui.forecast.time.get_date_time(ui.forecast.weather.dt)
        # ui.text_right(16, '{:d}.{:d}.{:d} {:d}:{:02d}'.format(dt[2], dt[1], dt[0], dt[3], dt[4]), Vect(self.dim.x, 25))
