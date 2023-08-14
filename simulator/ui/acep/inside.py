from ulogging import getLogger

logger = getLogger(__name__)

from micropython import const
from .. import UiFrame, V, BLUE
from .vbat import UiVBat
from .rh import UiRh
from db import location


class UiInside(UiFrame):
    def draw(self, connection, volt, layout_2):
        SPACING = const(18)
        spacing = self.height // (2 if layout_2 else 3) + 1

        # Type humidity
        rh = UiRh(self.ui, V(0, self.height - spacing), V(self.width, spacing))
        rh.repaint(self.ui.forecast.home.rh)

        # Display battery state
        if layout_2:
            batt = UiVBat(self.ui, V(self.width - 40, 8), V(24, 36))
        else:
            batt = UiVBat(self.ui, V(self.width - 40, 0), V(24, 36))
        batt.repaint(volt)

        # Type weather details
        dt = self.ui.forecast.time.get_date_time(self.ui.forecast.weather.dt)
        dt = f"{dt[2]:d}.{dt[1]:d}.{dt[0]:d} {dt[3]:d}:{dt[4]:02d}"

        if layout_2:
            y = self.dim.y - 20
            self.ui.text(16, dt, V(5, y))
            y -= SPACING
            self.ui.text(
                16, location.LOCATIONS[connection.config.location].name, V(5, y), BLUE
            )
        else:
            y = batt.bellow + 4
            x = self.dim.x - 2
            self.ui.text_right(
                16, location.LOCATIONS[connection.config.location].name, V(x, y), BLUE
            )
            y += SPACING
            self.ui.text_right(16, dt, V(x, y))
