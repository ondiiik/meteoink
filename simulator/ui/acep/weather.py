from ulogging import getLogger

logger = getLogger(__name__)

from .. import UiFrame, Vect


class UiWeather(UiFrame):
    def draw(self, connection, wdt):
        connection.disconnect()
        wdt.feed()
        weather = self.ui.forecast.weather
        bitmap = self.ui.bitmap(1, weather.icon)
        self.canvas.bitmap(Vect(5, 0), bitmap)
