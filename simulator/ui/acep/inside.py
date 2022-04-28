from ulogging import getLogger
logger = getLogger(__name__)

from micropython import const
from .. import UiFrame, V, BLUE
from .vbat import UiVBat
from .rh import UiRh
from config import location


class UiInside(UiFrame):
    def draw(self, connection, volt):
        SPACING = const(18)

        # Type humidity
        rh = UiRh(self.ui, V(0, self.height - 35), V(self.width, 35))
        rh.repaint(self.ui.forecast.home.rh)

        # Display battery state
        batt = UiVBat(self.ui, V(self.width - 40, 0), V(24, 36))
        batt.repaint(volt)

        # Type weather details
        y = batt.bellow + 4
        x = self.dim.x - 2
        self.ui.text_right(16, location[connection.config.location].name, V(x, y), BLUE)
        y += SPACING
        dt = self.ui.forecast.time.get_date_time(self.ui.forecast.weather.dt)
        self.ui.text_right(16, f'{dt[2]:d}.{dt[1]:d}.{dt[0]:d} {dt[3]:d}:{dt[4]:02d}', V(x, y))
