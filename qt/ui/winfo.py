from   ui          import UiFrame, Vect
from   micropython import const
import micropython 

_INSIDE_OFS_A  = const(70)
_INSIDE_OFS_80 = const(-10)
_INSIDE_OFS_B  = const(_INSIDE_OFS_A  + 10)
_INSIDE_OFS_50 = const(_INSIDE_OFS_80 + 20)


@micropython.native
class UiWInfo(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
    def draw(self, ui, args):
        fcast = ui.forecast
        
        ui.text(25, '{},  {}'.format(fcast.location, fcast.descr), Vect(0, 25))
        dt = fcast.time.get_date_time(fcast.weather.dt)
        ui.text(25, '{:d}.{:d}.{:d} {:d}:{:02d}'.format(dt[2], dt[1], dt[0], dt[3], dt[4]), Vect(0, 0))
