from ulogging import getLogger

logger = getLogger(__name__)

from ui import UiFrame, Vect, with_forecast


class UiWeather(UiFrame):
    @with_forecast
    def draw(self, forecast, connection, wdt):
        connection.disconnect()
        wdt.feed()
        weather = forecast.weather
        bitmap = self.ui.bitmap(1, weather.icon)
        self.canvas.bitmap(Vect(5, 0), bitmap)
