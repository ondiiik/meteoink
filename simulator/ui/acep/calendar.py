from ulogging import getLogger

logger = getLogger(__name__)

from .. import UiFrame, V, Z, BLACK, GREEN
from micropython import const
from lang import day_of_week
from config import api


class UiCalendar(UiFrame):
    def draw(self, show_days):
        forecast = self.ui.forecast.forecast
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
            self.canvas.hline(Z, self.dim.x - 1)

        # Find time related to next day
        week_day = self.ui.forecast.time.get_date_time(forecast[0].dt)[6]

        for i in range(len(forecast)):
            dt = self.ui.forecast.time.get_date_time(forecast[i].dt)
            if not week_day == dt[6]:
                dh = dt[3]
                break

        # Draw all items related to forecast
        first = True
        for x, f in self.ui.forecast_singles():
            dt = self.ui.forecast.time.get_date_time(f.dt)
            hour = dt[3] - dh

            # Draw weekends
            if show_days and ((dt[6] == 5) or (dt[6] == 6)):
                if first:
                    self.canvas.trect(
                        V(int(x - dt[3] // hpi * hpi * block / hpi), 1),
                        V(dblock, 26),
                        GREEN,
                    )
                if 0 == hour:
                    self.canvas.trect(V(x, 1), V(dblock, 26), GREEN)

            # Draw separators
            sep_space = self.dim.y + h_space - (20 if show_days else 10)
            if 0 == hour:
                if (dt[6] == 5) or (dt[6] == 0):
                    self.canvas.vline(V(x + 1, 0), sep_space, BLACK)

                self.canvas.vline(V(x, 0), sep_space, BLACK)

            if show_days:
                # Draw hours text
                if hour % 6 == 0:
                    self.ui.text_center(16, str(hour), V(x, self.dim.y // 2 + h_space))

                # Draw day of week text
                if (hour + 12) % 24 == 0:
                    self.ui.text_center(16, day_of_week[dt[6]], V(x, h_space))

            first = False
