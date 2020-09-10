from ui          import UiFrame, Vect, Color
from micropython import const

class UiTempGr(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
    def draw(self, ui, d):
        # Pre-calculates some range values and draw icons bar
        forecast = ui.forecast.forecast
        cnt      = len(forecast)
        block    = ui.canvas.dim.x / cnt
        temp_max = -273.0
        temp_min =  273.0
        
        for i1 in range(cnt):
            xx       = ui.canvas.dim.x * i1 // (cnt + 1)
            weather  = forecast[i1]
            temp_max = max(weather.max, temp_max)
            temp_min = min(weather.min, temp_min)
        
        chart_space    = const(30)
        chart_min      = const(chart_space // 2)
        self.chart_max = self.dim.y - chart_space
        self.k_temp    = (self.chart_max - chart_min) / (temp_max - temp_min)
        
        
        # Get chart position according to temperature
        def chart_y(temp):
            return int(self.chart_max - (temp - temp_min) * self.k_temp)
        
        for i1 in range(cnt):
            # Draw temp and temp feels like chart shadow
            if i1 > 0:
                x1 = int(block  * i1)
                x2 = int(x1 - block)
                i2 = i1 - 1
                
                v1 = Vect(x1, chart_y(forecast[i1].feel))
                v2 = Vect(x2, chart_y(forecast[i2].feel))
                ui.canvas.line(v1, v2, Color.WHITE, 2)
                
                v1 = Vect(x1, chart_y(forecast[i1].temp))
                v2 = Vect(x2, chart_y(forecast[i2].temp))
                ui.canvas.line(v1, v2, Color.WHITE, 4)
        
        for i1 in range(cnt):
            # Highlight extremes in temp chart
            if i1 > 0:
                x1 = int(block  * i1)
                x2 = int(x1 - block)
                i2 = i1 - 1
                
                v1 = Vect(x1, chart_y(forecast[i1].temp))
                v2 = Vect(x2, chart_y(forecast[i2].temp))
                
                if (forecast[i1].max > 27) or \
                   (forecast[i2].max > 27) or \
                   (forecast[i1].min < -5) or \
                   (forecast[i2].min < -5):
                    ui.canvas.line(v1, v2, Color.YELLOW, 6)
        
        for i1 in range(cnt):
            x1 = int(block  * i1)
            x2 = int(x1 - block)
            i2 = i1 - 1
            
            # Draw temp and temp feels like chart
            if i1 > 0:
                v1 = Vect(x1, chart_y(forecast[i1].feel))
                v2 = Vect(x2, chart_y(forecast[i2].feel))
                ui.canvas.line(v1, v2, Color.BLACK, 1)
                
                v1 = Vect(x1, chart_y(forecast[i1].temp))
                v2 = Vect(x2, chart_y(forecast[i2].temp))
                ui.canvas.line(v1, v2, Color.BLACK, 2)
