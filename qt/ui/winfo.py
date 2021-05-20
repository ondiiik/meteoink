from ui          import UiFrame, Vect
from config      import location
from micropython import const


_INSIDE_OFS_A  = const(70)
_INSIDE_OFS_80 = const(-10)
_INSIDE_OFS_B  = const(_INSIDE_OFS_A  + 10)
_INSIDE_OFS_50 = const(_INSIDE_OFS_80 + 20)


class UiWInfo(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
    def draw(self, ui, args):
        ui.text(25, ui.forecast.descr, Vect(0, 25))
        dt = ui.forecast.time.get_date_time(ui.forecast.weather.dt)
        ui.text(25, '{:d}.{:d}.{:d} {:d}:{:02d}'.format(dt[2], dt[1], dt[0], dt[3], dt[4]), Vect(0, 0))
