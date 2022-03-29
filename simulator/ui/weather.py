from ui import UiFrame, Vect, BLACK, WHITE
from forecast import id2icon


class UiWeather(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)

    def draw(self, ui, d):
        weather = ui.forecast.weather
        bitmap = ui.bitmap(1, weather.icon)
        ui.canvas.bitmap(Vect(5, 0), bitmap)

        if weather.rain > 0:
            ui.text(10, '{:.1f} mm/h'.format(weather.rain), Vect(2, self.dim.y - 14), BLACK, WHITE)
