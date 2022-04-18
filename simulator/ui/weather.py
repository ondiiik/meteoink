from ui import UiFrame, Vect, BLACK, WHITE


class UiWeather(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)

    def draw(self, ui, d):
        weather = ui.forecast.weather
        bitmap = ui.bitmap(1, weather.icon)
        ui.canvas.bitmap(Vect(5, 0), bitmap)

        if weather.rain > 0:
            ui.text(10, f'{weather.rain:.1f} mm/h', Vect(2, self.dim.y - 14), BLACK, WHITE)
