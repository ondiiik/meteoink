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

        self.ui.text(60, t, ZERO)
        self.ui.text(25, "%", Vect(80, 15))

        # Type weather details
        self.ui.text_right(25, forecast.descr, Vect(self.dim.x, self.dim.y - 80))
        self.ui.text_right(
            25,
            location["locations"][connection.config["location"]]["name"],
            Vect(self.dim.x, self.dim.y - 30),
        )
        dt = forecast.time.get_date_time(forecast.weather.dt)
        self.ui.text_right(
            25,
            "{:d}.{:d}.{:d} {:d}:{:02d}".format(dt[2], dt[1], dt[0], dt[3], dt[4]),
            Vect(self.dim.x, self.dim.y - 55),
        )

        batt = UiVBat(self.ui, Vect(18, self.height - 30), Vect(25, 16))
        batt.repaint(volt)
