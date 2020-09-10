from ui          import UiFrame, Vect, Color
from micropython import const

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
            temp_max = max(weather.max, temp_max)
            temp_min = min(weather.min, temp_min)
        
        chart_space  = const(30)
        chart_min    = const(chart_space // 2)
        chart_max    = self.dim.y - chart_space
        k_temp       = (chart_max - chart_min) / (temp_max - temp_min)
        
        
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
                
                if (f[0].max < f[1].max) and (f[1].max > f[2].max):
                    ui.text_center(10, '{:.0f}°C'.format(f[1].max), Vect(x1, chart_y(f[1].max) - 12), Color.BLACK, Color.WHITE)
                    
                if (f[0].min > f[1].min) and (f[1].min < f[2].min):
                    ui.text_center(10, '{:.0f}°C'.format(f[1].min), Vect(x1, chart_y(f[1].min) + 4),  Color.BLACK, Color.WHITE)
