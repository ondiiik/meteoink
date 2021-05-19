from ui          import UiFrame, Vect
from micropython import const


_OUTSIDE_OFS_A   = const(200)
_OUTSIDE_OFS_80  = const(-10)
_OUTSIDE_OFS_B   = const(_OUTSIDE_OFS_A  + 10)
_OUTSIDE_OFS_C   = const(_OUTSIDE_OFS_A  - 210)
_OUTSIDE_OFS_D   = const(_OUTSIDE_OFS_C  + 10)
_OUTSIDE_OFS_50  = const(_OUTSIDE_OFS_80 + 20)


class UiOutside(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
    def draw(self, ui, d):
        # Type humidity
        weather = ui.forecast.weather
        
        ui.text_right(80, '{:.0f}'.format(weather.rh),    Vect(_OUTSIDE_OFS_A, _OUTSIDE_OFS_80))
        ui.text(      50,  '% RH',                        Vect(_OUTSIDE_OFS_B, _OUTSIDE_OFS_50))
        
        # Type wind speed
        ui.text_right(80, '{:.1f}'.format(weather.speed), Vect(_OUTSIDE_OFS_C, _OUTSIDE_OFS_80))
        ui.text(      50, 'm/s',                          Vect(_OUTSIDE_OFS_D, _OUTSIDE_OFS_50))
