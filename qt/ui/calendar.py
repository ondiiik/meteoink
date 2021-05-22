from ui          import UiFrame, Vect, BLACK, GRAY
from micropython import const
from config      import ui as cfg
from config      import VARIANT_2DAYS


_CALENDAR_H_SPACE    = const(4)
_CALENDAR_DAY_FONT   = const(25)
_CALENDAR_HOUR_FONT  = const(25)

_CALENDAR_TITLE_SIZE = const(_CALENDAR_H_SPACE * 3 + _CALENDAR_DAY_FONT)
_CALENDAR_H_SEP_SIZE = const(_CALENDAR_DAY_FONT - 10 - _CALENDAR_H_SPACE)


class UiCalendar(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
        
    def draw(self, ui, title):
        if title:
            from lang import day_of_week
        
        forecast = ui.forecast.forecast
        cnt      = len(forecast)
        block    = ui.canvas.dim.x / cnt
        
        if cfg.variant == VARIANT_2DAYS:
            dblock = int(block * 24)
        else:
            dblock = int(block * 8)
        
        # Draw upper horizontal lines
        if title:
            ui.canvas.fill_rect(Vect(0, -5),                        Vect(self.dim.x - 1, 2), BLACK)
            ui.canvas.fill_rect(Vect(0,  0),                        Vect(self.dim.x - 1, 2), BLACK)
            ui.canvas.fill_rect(Vect(0,  _CALENDAR_TITLE_SIZE + 2), Vect(self.dim.x - 1, 2), GRAY)
        
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
            if 0 == hour or 0 == i:
                if title and ((dt[6] == 5) or (dt[6] == 6)):
                    ui.canvas.fill_rect(Vect(xx, 2), Vect(dblock, _CALENDAR_TITLE_SIZE), GRAY)
                
            if 0 == hour:
                c = BLACK if (dt[6] == 5) or (dt[6] == 0) else GRAY
                ui.canvas.fill_rect(Vect(xx - 1, 2), Vect(3, self.dim.y + _CALENDAR_H_SEP_SIZE), c)
                ui.canvas.vline(Vect(xx, 0), self.dim.y + _CALENDAR_H_SEP_SIZE, BLACK)
            
            if title:
                # Draw hours text
                if hour % 6 == 0:
                    ui.text_center(_CALENDAR_HOUR_FONT, str(hour), Vect(xx, self.dim.y // 2 + _CALENDAR_DAY_FONT))
                
                # Draw day of week text
                if (hour + 12) % 24 == 0:
                    ui.text_center(_CALENDAR_DAY_FONT, day_of_week[dt[6]], Vect(xx, _CALENDAR_H_SPACE))
