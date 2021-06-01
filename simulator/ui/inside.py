from ui     import UiFrame, Vect
from config import location

class UiInside(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
    def draw(self, ui, args):
        tab, connection = args
        
        # Type celsius symbol
        ui.text(50, '°C', Vect(111, -5))
        
        # Type humidity
        if None == ui.forecast.home.rh:
            t = '--'
        else:
            t = '{:.0f}'.format(ui.forecast.home.rh)
            
        ui.text(25, t, Vect(175, 0))
        ui.text(10, '%',  Vect(175 + tab, 11))
        
        
        # Type weather details
        ui.text_right(10, ui.forecast.descr, Vect(self.dim.x, 15))
        ui.text_right(10, location[connection.config.location].name, Vect(self.dim.x, 35))
        dt = ui.forecast.time.get_date_time(ui.forecast.weather.dt)
        ui.text_right(10, '{:d}.{:d}.{:d} {:d}:{:02d}'.format(dt[2], dt[1], dt[0], dt[3], dt[4]), Vect(self.dim.x, 25))
