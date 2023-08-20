from ulogging import getLogger

logger = getLogger(__name__)

from .. import UiFrame, Vect
from display.epd import BLACK, WHITE


class UiTempTxt(UiFrame):
    def draw(self, graph_temp):
        for x, fl, f, fr in self.ui.forecast_tripples():
            if (fl.temp < f.temp) and (f.temp > fr.temp):
                self.ui.text_center(
                    25,
                    "{:.0f}°C".format(f.temp),
                    Vect(x, graph_temp.chart_y(f.temp) - 40),
                    BLACK,
                )

            if (fl.temp > f.temp) and (f.temp < fr.temp):
                self.ui.text_center(
                    25,
                    "{:.0f}°C".format(f.temp),
                    Vect(x, graph_temp.chart_y(f.temp) + 4),
                    BLACK,
                )
