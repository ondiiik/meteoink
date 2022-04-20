from ulogging import getLogger
logger = getLogger(__name__)

from ui import UiFrame, Vect as V, BLACK, WHITE


class UiWeather(UiFrame):
    def draw(self, ui):
        weather = ui.forecast.weather
        bitmap = ui.bitmap(1, weather.icon)
        ui.canvas.bitmap(V(5, 0), bitmap)

        if weather.rain > 0:
            ui.text(10, f'{weather.rain:.1f} mm/h', V(2, self.dim.y - 14), BLACK, WHITE)
