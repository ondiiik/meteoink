from ui import UiFrame, Vect, BLACK, WHITE, YELLOW

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
            xx      = int(block * i)
            weather = forecast[i]
            dt      = ui.forecast.time.get_date_time(weather.dt)
            
            # Draw rain chart
            p = max(weather.rain, weather.snow)
            
            if weather.rain > 0 or weather.snow > 0:
                r = int(p * 12)
                _ = self.dim.y // 4
                for h in (_, _ * 2, _ * 3):
                    if r > h:
                        r = h + (r - h) // 2
                v = Vect(xx - int(block // 2) + 1, self.dim.y - r - 1)
                d = Vect(int(block) - 2, r)
                
                if weather.rain > 0:
                    ui.canvas.trect(v, d, BLACK)
                else:
                    ui.canvas.fill_rect(v, d, YELLOW)
                ui.canvas.rect( v, d, BLACK)
            
            # Type rain text
            if (i > 0) and (i < cmax):
                f0 = forecast[i - 1]
                f1 = forecast[i + 1]
                if (max(f0.rain, f0.snow) < p) and (p > max(f1.rain, f1.snow)): 
                    ui.text_center(10, '%.1f' % p, Vect(xx, self.dim.y - 2), BLACK, WHITE)
