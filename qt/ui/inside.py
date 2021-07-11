from   ui          import UiFrame, Vect
from   micropython import const
import micropython 


_INSIDE_OFS_A  = const(70)
_INSIDE_OFS_80 = const(-10)
_INSIDE_OFS_B  = const(_INSIDE_OFS_A  + 10)
_INSIDE_OFS_50 = const(_INSIDE_OFS_80 + 20)


class UiInside(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
    @micropython.native
    def draw(self, ui, args):
        t = '--' if ui.forecast.home.rh is None else '{:.0f}'.format(ui.forecast.home.rh)
        ui.text_right(80, t,      Vect(_INSIDE_OFS_A, _INSIDE_OFS_80))
        ui.text(      50, '% RH', Vect(_INSIDE_OFS_B, _INSIDE_OFS_50))
