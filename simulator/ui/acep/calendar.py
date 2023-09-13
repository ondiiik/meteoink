from ulogging import getLogger

logger = getLogger(__name__)

from ui import UiFrame, Vect, ZERO, with_forecast
from display.epd import BLACK, GREEN
from micropython import const
from lang import day_of_week
from config import api


class UiCalendar(UiFrame):
    @with_forecast
    def draw(self, forecast, show_days):
        block = self.ui.block
        h_space = const(4)

        if api["variant"] == 2:
            hpi = 1
            dblock = int(block * 24)
        else:
            hpi = 3
            dblock = int(block * 8)

        # Draw upper horizontal lines
        if show_days:
            self.canvas.hline(ZERO, self.dim.x - 1)

        # Find time related to next day
        week_day = forecast.time.get_date_time(forecast.forecast[0].dt)[6]

        for i in range(len(forecast.forecast)):
            dt = forecast.time.get_date_time(forecast.forecast[i].dt)
            if not week_day == dt[6]:
                dh = dt[3]
                break

        # Draw all items related to forecast
        first = True
        for x, f in self.ui.forecast_singles():
            dt = forecast.time.get_date_time(f.dt)
            hour = dt[3] - dh

            # Draw weekends
            if show_days and ((dt[6] == 5) or (dt[6] == 6)):
                if first:
                    self.canvas.trect(
                        Vect(int(x - dt[3] // hpi * hpi * block / hpi), 1),
                        Vect(dblock, 26),
                        GREEN,
                    )
                if 0 == hour:
                    self.canvas.trect(Vect(x, 1), Vect(dblock, 26), GREEN)

            # Draw separators
            sep_space = self.dim.y + h_space - (20 if show_days else 10)
            if 0 == hour:
                if (dt[6] == 5) or (dt[6] == 0):
                    self.canvas.vline(Vect(x + 1, 0), sep_space, BLACK)

                self.canvas.vline(Vect(x, 0), sep_space, BLACK)

            if show_days:
                # Draw hours text
                if hour % 6 == 0:
                    self.ui.text_center(
                        16, str(hour), Vect(x, self.dim.y // 2 + h_space)
                    )

                # Draw day of week text
                if (hour + 12) % 24 == 0:
                    self.ui.text_center(16, day_of_week[dt[6]], Vect(x, h_space))

            first = False
