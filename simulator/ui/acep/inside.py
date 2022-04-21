from ulogging import getLogger
logger = getLogger(__name__)

from .. import UiFrame, Vect as V, BLUE
from .vbat import UiVBat
from config import location


class UiInside(UiFrame):
    def draw(self, connection, volt):
        # Type humidity
        if None == self.ui.forecast.home.rh:
            t = '--'
        else:
            t = '{:.0f}'.format(self.ui.forecast.home.rh)

        self.ui.text(25, t, V(0, 0))
        self.ui.text(10, '%',  V(32, 11))

        # Type weather details
        self.ui.text_right(10, self.ui.forecast.descr, V(self.dim.x, self.height - 38), BLUE)
        self.ui.text_right(10, location[connection.config.location].name, V(self.dim.x, self.height - 26), BLUE)
        dt = self.ui.forecast.time.get_date_time(self.ui.forecast.weather.dt)
        self.ui.text_right(10, '{:d}.{:d}.{:d} {:d}:{:02d}'.format(dt[2], dt[1], dt[0], dt[3], dt[4]), V(self.dim.x, self.height - 15), BLUE)

        # Display battery state
        batt = UiVBat(self.ui, V(6, self.height - 26), V(14, 10))
        batt.repaint(volt)
