from ulogging import getLogger
logger = getLogger(__name__)

from .. import UiFrame, V, BLACK, WHITE
from micropython import const


class UiTempTxt(UiFrame):
    def draw(self):
        # Pre-calculates some range values and draw icons bar
        forecast = self.ui.forecast.forecast
        cnt = len(forecast)
        temp_max = -273.0
        temp_min = 273.0

        for i in range(cnt):
            weather = forecast[i]
            temp_max = max(weather.temp, weather.feel, temp_max)
            temp_min = min(weather.temp, weather.feel, temp_min)

        chart_space = const(30)
        chart_min = const(chart_space // 2)
        chart_max = self.dim.y - chart_space
        k_temp = (chart_max - chart_min) / (temp_max - temp_min)

        # Get chart position according to temperature
        def chart_y(temp):
            return int(chart_max - (temp - temp_min) * k_temp)

        for x, fl, f, fr in self.ui.forecast_tripples():
            if (fl.temp < f.temp) and (f.temp > fr.temp):
                self.ui.text_center(16, '{:.0f}°C'.format(f.temp), V(x, chart_y(f.temp) - 20), BLACK, WHITE)

            if (fl.temp > f.temp) and (f.temp < fr.temp):
                self.ui.text_center(16, '{:.0f}°C'.format(f.temp), V(x, chart_y(f.temp) + 4),  BLACK, WHITE)
