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
            t = f"{forecast.home.rh:.0f}"

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
            f"{dt[2]:d}.{dt[1]:d}.{dt[0]:d} {dt[3]:d}:{dt[4]:02d}",
            Vect(self.dim.x, 25),
        )

        batt = UiVBat(self.ui, Vect(6, self.height - 26), Vect(14, 10))
        batt.repaint(volt)
