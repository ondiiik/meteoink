from ulogging import getLogger
logger = getLogger(__name__)

from ui import UiFrame, Vect as V
from config import location


class UiInside(UiFrame):
    def draw(self, ui, tab, connection):
        # Type celsius symbol
        ui.text(50, '°C', V(111, -5))

        # Type humidity
        if None == ui.forecast.home.rh:
            t = '--'
        else:
            t = '{:.0f}'.format(ui.forecast.home.rh)

        ui.text(25, t, V(175, 0))
        ui.text(10, '%',  V(175 + tab, 11))

        # Type weather details
        ui.text_right(10, ui.forecast.descr, V(self.dim.x, 15))
        ui.text_right(10, location[connection.config.location].name, V(self.dim.x, 35))
        dt = ui.forecast.time.get_date_time(ui.forecast.weather.dt)
        ui.text_right(10, '{:d}.{:d}.{:d} {:d}:{:02d}'.format(dt[2], dt[1], dt[0], dt[3], dt[4]), V(self.dim.x, 25))
