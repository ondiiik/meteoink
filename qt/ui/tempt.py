from ui          import UiFrame, Vect
from micropython import const


_CHART_SPACE    = const(-20)
_CHART_MIN      = const(_CHART_SPACE // 2)
_CHART_OVERSHOT = const(12 - _CHART_SPACE)


class UiTempTxt(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
    def draw(self, ui, d):
        # Pre-calculates some range values and draw icons bar
        forecast = ui.forecast.forecast
        cnt      = len(forecast)
        block    = ui.canvas.dim.x / cnt
        temp_max = -273.0
        temp_min =  273.0
        
        for i in range(cnt):
            x1       = ui.canvas.dim.x * i // (cnt + 1)
            weather  = forecast[i]
            temp_max = max(weather.temp, weather.feel, temp_max)
            temp_min = min(weather.temp, weather.feel, temp_min)
        
        chart_max    = self.dim.y - _CHART_OVERSHOT
        k_temp       = (chart_max - _CHART_MIN) / (temp_max - temp_min)
        
        
        # Get chart position according to temperature
        def chart_y(temp):
            return int(chart_max - (temp - temp_min) * k_temp)
        
        for i in range(cnt):
            cmax = cnt - 1
            x1   = int(block * i)
            
            # Calculate and type peaks
            if (i > 0) and (i < cmax):
                # Draw temperature text
                f = (forecast[i-1], forecast[i], forecast[i+1])
                
                if (f[0].temp < f[1].temp) and (f[1].temp > f[2].temp):
                    ui.text_center(25, '{:.0f}°C'.format(f[1].temp), Vect(x1, chart_y(f[1].temp) - 26))
                    
                if (f[0].temp > f[1].temp) and (f[1].temp < f[2].temp):
                    ui.text_center(25, '{:.0f}°C'.format(f[1].temp), Vect(x1, chart_y(f[1].temp) + 6))
