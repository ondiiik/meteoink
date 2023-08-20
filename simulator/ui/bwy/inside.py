from ulogging import getLogger

logger = getLogger(__name__)

from .. import UiFrame, Vect, ZERO
from .vbat import UiVBat
from config import location


class UiInside(UiFrame):
    def draw(self, connection, volt):
        # Type humidity
        if None == self.ui.forecast.home.rh:
            t = "--"
        else:
            t = "{:.0f}".format(self.ui.forecast.home.rh)

        self.ui.text(25, t, ZERO)
        self.ui.text(10, "%", Vect(32, 11))

        # Type weather details
        self.ui.text_right(10, self.ui.forecast.descr, Vect(self.dim.x, 15))
        self.ui.text_right(
            10,
            location["locations"][connection.config["location"]]["name"],
            Vect(self.dim.x, 35),
        )
        dt = self.ui.forecast.time.get_date_time(self.ui.forecast.weather.dt)
        self.ui.text_right(
            10,
            "{:d}.{:d}.{:d} {:d}:{:02d}".format(dt[2], dt[1], dt[0], dt[3], dt[4]),
            Vect(self.dim.x, 25),
        )

        batt = UiVBat(self.ui, Vect(6, self.height - 26), Vect(14, 10))
        batt.repaint(volt)
