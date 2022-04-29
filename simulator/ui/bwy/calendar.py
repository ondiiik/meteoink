from ulogging import getLogger
logger = getLogger(__name__)

from .. import UiFrame, BLACK, V, Z
from micropython import const
from lang import day_of_week
from db import ui


class UiCalendar(UiFrame):
    def draw(self, show_days):
        forecast = self.ui.forecast.forecast
        cnt = len(forecast)
        block = self.ui.block
        h_space = const(4)

        if ui.VARIANT == 2:
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

        for i in forecast:
            dt = self.ui.forecast.time.get_date_time(i.dt)
            if not week_day == dt[6]:
                dh = dt[3]
                break

        # Draw all items related to forecast
        for i in range(cnt):
            xx = int(block * i)
            weather = forecast[i]
            dt = self.ui.forecast.time.get_date_time(weather.dt)
            hour = dt[3] - dh

            # Draw separators
            if show_days and ((dt[6] == 5) or (dt[6] == 6)):
                if 0 == i:
                    self.canvas.trect(V(int(xx - dt[3] // hpi * hpi * block / hpi), 1), V(dblock, 4), BLACK)
                if 0 == hour:
                    self.canvas.trect(V(xx, 1), V(dblock, 4), BLACK)

            if 0 == hour:
                if (dt[6] == 5) or (dt[6] == 0):
                    self.canvas.vline(V(xx + 1, 0), self.dim.y - 10 + h_space, BLACK)

                self.canvas.vline(V(xx, 0), self.dim.y - 10 + h_space, BLACK)

            if show_days:
                # Draw hours text
                if hour % 6 == 0:
                    self.ui.text_center(10, str(hour), V(xx, self.dim.y // 2 + h_space + 6))

                # Draw day of week text
                if (hour + 12) % 24 == 0:
                    self.ui.text_center(16, day_of_week[dt[6]], V(xx, h_space))
