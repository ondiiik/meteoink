from ulogging import getLogger
logger = getLogger(__name__)

from micropython import const
from .. import UiFrame, Vect as V, BLUE, RED, GREEN, BLACK
from .vbat import UiVBat
from config import location


class UiInside(UiFrame):
    def draw(self, connection, volt):
        SPACING = const(18)
        LOWERING = const(13)
        SYMDIST = const(46)

        # Type humidity
        if None == self.ui.forecast.home.rh:
            c = BLACK
            t = '--'
        else:
            v = round(self.ui.forecast.home.rh)
            c = GREEN if v in range(45, 60) else BLUE if v in range(40, 65) else RED
            t = f'{self.ui.forecast.home.rh:.0f}'

        self.ui.text_right(35, t, V(self.width - 2 - SYMDIST, self.height - 35), c)
        self.ui.text_right(16, '%RH',  V(self.width - 2, self.height - 24))

        # Display battery state
        batt = UiVBat(self.ui, V(self.width - 32, 0), V(24, 30))
        batt.repaint(volt)

        # Type weather details
        y = batt.bellow + 4
        x = self.dim.x - 2
        self.ui.text_right(16, location[connection.config.location].name, V(x, y), BLUE)
        y += SPACING
        dt = self.ui.forecast.time.get_date_time(self.ui.forecast.weather.dt)
        self.ui.text_right(16, f'{dt[2]:d}.{dt[1]:d}.{dt[0]:d} {dt[3]:d}:{dt[4]:02d}', V(x, y))
