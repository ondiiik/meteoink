from ulogging import getLogger
logger = getLogger(__name__)

from .. import UiFrame, Vect as V, BLUE, RED, GREEN, BLACK
from .vbat import UiVBat
from config import location


class UiInside(UiFrame):
    def draw(self, connection, volt):
        # Type humidity
        if None == self.ui.forecast.home.rh:
            c = BLACK
            t = '--'
        else:
            v = round(self.ui.forecast.home.rh)
            c = GREEN if v in range(45, 60) else BLUE if v in range(40, 65) else RED
            t = f'{self.ui.forecast.home.rh:.0f}'

        self.ui.text(25, t, V(0, self.height - 25), c)
        self.ui.text(10, '%',  V(32, self.height - 14))

        # Type weather details
        self.ui.text_right(10, self.ui.forecast.descr, V(self.dim.x, self.height - 38))
        self.ui.text_right(10, location[connection.config.location].name, V(self.dim.x, self.height - 26), BLUE)
        dt = self.ui.forecast.time.get_date_time(self.ui.forecast.weather.dt)
        self.ui.text_right(10, '{:d}.{:d}.{:d} {:d}:{:02d}'.format(dt[2], dt[1], dt[0], dt[3], dt[4]), V(self.dim.x, self.height - 15))

        # Display battery state
        batt = UiVBat(self.ui, V(self.width - 26, 0), V(14, 10))
        batt.repaint(volt)
