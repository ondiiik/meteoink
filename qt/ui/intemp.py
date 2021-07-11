from   ui          import UiFrame, Vect, BLACK
from   micropython import const
import micropython 


_INTEMP_OFS_0   = const(-150)
_INTEMP_OFS_A   = const(170)
_INTEMP_OFS_160 = const(-30)
_INTEMP_OFS_B   = const(_INTEMP_OFS_A   + 10)
_INTEMP_OFS_120 = const(_INTEMP_OFS_160 + 20)


class UiInTemp(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
        
    @micropython.native
    def draw(self, ui, d):
        t = ui.forecast.home.temp
        t = '{:.1f}'.format(t) if not None == t else '--'
        ui.text_right(160, t,    Vect(_INTEMP_OFS_A, _INTEMP_OFS_160))
        ui.text(      120, '°C', Vect(_INTEMP_OFS_B, _INTEMP_OFS_120))
        ui.canvas.fill_rect(Vect(_INTEMP_OFS_0, 0), Vect(3, self.dim.y), BLACK)
