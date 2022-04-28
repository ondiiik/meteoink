from ulogging import getLogger
logger = getLogger(__name__)

from .. import UiFrame, V, BLACK, WHITE, RED
from micropython import const


class UiTempTxt(UiFrame):
    def draw(self):
        # Pre-calculates some range values and draw icons bar
        forecast = self.ui.forecast.forecast
        cnt = len(forecast)
        block = self.canvas.dim.x / cnt
        temp_max = -273.0
        temp_min = 273.0

        for i in range(cnt):
            x1 = self.canvas.dim.x * i // (cnt + 1)
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

        for i in range(cnt):
            cmax = cnt - 1
            x1 = int(block * i)

            # Calculate and type peaks
            if (i > 0) and (i < cmax):
                # Draw temperature text
                f = (forecast[i - 1], forecast[i], forecast[i + 1])

                if (f[0].temp < f[1].temp) and (f[1].temp > f[2].temp):
                    self.ui.text_center(16, '{:.0f}°C'.format(f[1].temp), V(x1, chart_y(f[1].temp) - 20), BLACK, WHITE)

                if (f[0].temp > f[1].temp) and (f[1].temp < f[2].temp):
                    self.ui.text_center(16, '{:.0f}°C'.format(f[1].temp), V(x1, chart_y(f[1].temp) + 4),  BLACK, WHITE)
