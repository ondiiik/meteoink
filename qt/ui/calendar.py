from ui          import UiFrame, Vect, Color
from forecast    import id2icon
from micropython import const


class UiCalendar(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
        
    def draw(self, ui, title):
        if title:
            wday2str = ('Pondělí',
                        'Úterý',
                        'Středa',
                        'Čtvrtek',
                        'Pátek',
                        'Sobota',
                        'Neděle')
        
        forecast = ui.forecast.forecast
        cnt     = len(forecast)
        block   = ui.canvas.dim.x / cnt
        h_space = const(4)
        
        # Draw upper horizontal lines
        if title:
            ui.canvas.hline(Vect(0, 0), self.dim.x - 1, Color.BLACK)
        
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
            if 0 == hour:
                if title:
                    if (dt[6] == 5) or (dt[6] == 6):
                        ui.canvas.trect(Vect(xx, 1), Vect(int(block * 8), 4), Color.BLACK)
                
                if (dt[6] == 5) or (dt[6] == 0):
                    ui.canvas.vline(Vect(xx + 1, 0), self.dim.y - 10 + h_space, Color.BLACK)
                
                ui.canvas.vline(Vect(xx, 0), self.dim.y - 10 + h_space, Color.BLACK)
            
            if title:
                # Draw hours text
                if hour % 6 == 0:
                    ui.text_center(10, str(hour), Vect(xx, self.dim.y // 2 + h_space))
                
                # Draw day of week text
                if (hour + 12) % 24 == 0:
                    ui.text_center(10, wday2str[dt[6]], Vect(xx, h_space))
