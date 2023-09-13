from ulogging import getLogger

logger = getLogger(__name__)

from micropython import const
from ui import UiFrame, Vect, with_forecast
from display.epd import BLUE
from .vbat import UiVBat
from .rh import UiRh
from config import location


class UiInside(UiFrame):
    @with_forecast
    def draw(self, forecast, connection, volt, layout_2):
        SPACING = const(18)
        spacing = self.height // (2 if layout_2 else 3) + 1

        # Type humidity
        rh = UiRh(self.ui, Vect(0, self.height - spacing), Vect(self.width, spacing))
        rh.repaint(forecast.home.rh)

        # Display battery state
        if layout_2:
            batt = UiVBat(self.ui, Vect(self.width - 40, 8), Vect(24, 36))
        else:
            batt = UiVBat(self.ui, Vect(self.width - 40, 0), Vect(24, 36))
        batt.repaint(volt)

        # Type weather details
        dt = forecast.time.get_date_time(forecast.weather.dt)
        dt = f"{dt[2]:d}.{dt[1]:d}.{dt[0]:d} {dt[3]:d}:{dt[4]:02d}"

        if layout_2:
            y = self.dim.y - 20
            self.ui.text(16, dt, Vect(5, y))
            y -= SPACING
            self.ui.text(
                16,
                location["locations"][connection.config["location"]]["name"],
                Vect(5, y),
                BLUE,
            )
        else:
            y = batt.bellow + 4
            x = self.dim.x - 2
            self.ui.text_right(
                16,
                location["locations"][connection.config["location"]]["name"],
                Vect(x, y),
                BLUE,
            )
            y += SPACING
            self.ui.text_right(16, dt, Vect(x, y))
