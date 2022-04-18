from ui import UiFrame, Vect as V
from ui.wind import drawWind


class UiOutside(UiFrame):
    def draw(self, ui):
        # Draw wind
        weather = ui.forecast.weather
        drawWind(ui, V(260, 35), weather)

        # Type celsius symbol
        ui.text(50, '°C', V(111, -5))

        # Type humidity
        t = '{:.0f}'.format(weather.rh)
        ui.text(25, t, V(175, 18))
        l = ui.textLength(25, t) + 6
        ui.text(10, '%',  V(175 + l, 31))

        # Type wind speed
        ui.text(25, '{:.1f}'.format(weather.speed), V(175, -5))
        ui.text(10, 'm/s', V(175 + l, 8))

        return l
