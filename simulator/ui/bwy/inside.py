from ulogging import getLogger

logger = getLogger(__name__)

from ui import UiFrame, Vect, ZERO, with_forecast
from .vbat import UiVBat
from config import location


class UiInside(UiFrame):
    @with_forecast
    def draw(self, forecast, connection, volt):
        # Type humidity
        if None == forecast.home.rh:
            t = "--"
        else:
            t = "{:.0f}".format(forecast.home.rh)

        self.ui.text(25, t, ZERO)
        self.ui.text(10, "%", Vect(32, 11))

        # Type weather details
        self.ui.text_right(10, forecast.descr, Vect(self.dim.x, 15))
        self.ui.text_right(
            10,
            location["locations"][connection.config["location"]]["name"],
            Vect(self.dim.x, 35),
        )
        dt = forecast.time.get_date_time(forecast.weather.dt)
        self.ui.text_right(
            10,
            "{:d}.{:d}.{:d} {:d}:{:02d}".format(dt[2], dt[1], dt[0], dt[3], dt[4]),
            Vect(self.dim.x, 25),
        )

        batt = UiVBat(self.ui, Vect(6, self.height - 26), Vect(14, 10))
        batt.repaint(volt)
