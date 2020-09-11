from ui          import UiFrame, Vect, Color
from ui.wind     import drawWind
from micropython import const


class UiOutside(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
    def draw(self, ui, d):
        # Draw wind
        weather = ui.forecast.weather
        drawWind(ui, Vect(260, 35), weather)
        
        # Type celsius symbol
        ui.text(50, '°C', Vect(111, -5))
        
        # Type humidity
        t = '{:.0f}'.format(weather.rh)
        ui.text(25, t, Vect(175, 19))
        l = ui.textLength(25, t) + 6
        ui.text(10, '%',  Vect(175 + l, 32))
        
        # Type wind speed
        ui.text(25, '{:.1f}'.format(weather.speed), Vect(175, -5))
        ui.text(10, 'm/s', Vect(175 + l, 8))
        
        return l
