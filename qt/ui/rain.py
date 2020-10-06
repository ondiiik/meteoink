from ui import UiFrame, Vect, BLACK, WHITE
import         heap

class UiRain(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
        
    def draw(self, ui, d):
        # Pre-calculates some range values and draw icons bar
        forecast = ui.forecast.forecast
        cnt      = len(forecast)
        cmax     = cnt - 1
        block    = ui.canvas.dim.x / cnt
        
        ui.canvas.hline(Vect(0, self.dim.y - 1), self.dim.x - 1, BLACK)
        
        for i in range(cnt):
            heap.refresh()
            xx      = int(block * i)
            weather = forecast[i]
            dt      = ui.forecast.time.get_date_time(weather.dt)
            
            # Draw rain chart
            if weather.rain > 0:
                r = int(weather.rain * 12)
                _ = self.dim.y // 4
                for h in (_, _ * 2, _ * 3):
                    if r > h:
                        r = h + (r - h) // 2
                v = Vect(xx - int(block // 2) + 1, self.dim.y - r - 1)
                d = Vect(int(block) - 2, r)
                ui.canvas.rect( v, d, BLACK)
                ui.canvas.trect(v, d, BLACK)
            
            # Type rain text
            if (i > 0) and (i < cmax):
                if (forecast[i - 1].rain < weather.rain) and (weather.rain > forecast[i + 1].rain): 
                    ui.text_center(10, '%.1f' % weather.rain, Vect(xx, self.dim.y - 2), BLACK, WHITE)
