from ulogging import getLogger
logger = getLogger(__name__)

from .. import UiFrame, V


class UiWeather(UiFrame):
    def draw(self):
        weather = self.ui.forecast.weather
        bitmap = self.ui.bitmap(1, weather.icon)
        self.canvas.bitmap(V(5, 0), bitmap)
