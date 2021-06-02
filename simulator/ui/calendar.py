from ui          import UiFrame, Vect, BLACK
from micropython import const
from config      import ui as cfg
from config      import VARIANT_2DAYS


class UiCalendar(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
        
    def draw(self, ui, title):
        if title:
            from lang import day_of_week
        
        forecast = ui.forecast.forecast
        cnt     = len(forecast)
        block   = ui.canvas.dim.x / cnt
        h_space = const(4)
        
        if cfg.variant == VARIANT_2DAYS:
            hpi    = 1
            dblock = int(block * 24)
        else:
            hpi    = 3
            dblock = int(block * 8)
        
        # Draw upper horizontal lines
        if title:
            ui.canvas.hline(Vect(0, 0), self.dim.x - 1, BLACK)
        
        # Find time raleted to next day
        week_day = ui.forecast.time.get_date_time(forecast[0].dt)[6]
        
        for i in forecast:
            dt = ui.forecast.time.get_date_time(i.dt)
            if not week_day == dt[6]:
                dh = dt[3]
                break
        
        # Draw all items related to forecast
        for i in range(cnt):
            xx      = int(block * i)
            weather = forecast[i]
            dt      = ui.forecast.time.get_date_time(weather.dt)
            hour    = dt[3] - dh
            
            # Draw separators
            if title and ((dt[6] == 5) or (dt[6] == 6)):
                if 0 == i:
                    ui.canvas.trect(Vect(int(xx - dt[3] // hpi * hpi * block / hpi), 1), Vect(dblock, 4), BLACK)
                if 0 == hour:
                    ui.canvas.trect(Vect(xx, 1), Vect(dblock, 4), BLACK)
                
            if 0 == hour:
                if (dt[6] == 5) or (dt[6] == 0):
                    ui.canvas.vline(Vect(xx + 1, 0), self.dim.y - 10 + h_space, BLACK)
                
                ui.canvas.vline(Vect(xx, 0), self.dim.y - 10 + h_space, BLACK)
            
            if title:
                # Draw hours text
                if hour % 6 == 0:
                    ui.text_center(10, str(hour), Vect(xx, self.dim.y // 2 + h_space + 6))
                
                # Draw day of week text
                if (hour + 12) % 24 == 0:
                    ui.text_center(16, day_of_week[dt[6]], Vect(xx, h_space))
