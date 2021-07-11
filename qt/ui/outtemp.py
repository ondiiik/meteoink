from   ui          import UiFrame, Vect
from   config      import temp
from   micropython import const
import micropython 


_OUTTEMP_OFS_A   = const(200)
_OUTTEMP_OFS_120 = const(-30)
_OUTTEMP_OFS_B   = const(_OUTTEMP_OFS_A   + 10)
_OUTTEMP_OFS_80  = const(_OUTTEMP_OFS_120 + 20)


class UiOutTemp(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
        
    @micropython.native
    def draw(self, ui, d):
        t = ui.forecast.weather.temp
        ui.text_right(120, '{:.1f}'.format(t), Vect(_OUTTEMP_OFS_A, _OUTTEMP_OFS_120))
        ui.text(      80,  '°C',               Vect(_OUTTEMP_OFS_B, _OUTTEMP_OFS_80))