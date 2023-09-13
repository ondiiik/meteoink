from ulogging import getLogger

logger = getLogger(__name__)

from ui import UiFrame, Vect, with_forecast
from display.epd import BLACK, WHITE


class UiTempTxt(UiFrame):
    @with_forecast
    def draw(self, _, graph_temp):
        for x, fl, f, fr in self.ui.forecast_tripples():
            if (fl.temp < f.temp) and (f.temp > fr.temp):
                self.ui.text_center(
                    16,
                    "{:.0f}°C".format(f.temp),
                    Vect(x, graph_temp.chart_y(f.temp) - 20),
                    BLACK,
                    WHITE,
                )

            if (fl.temp > f.temp) and (f.temp < fr.temp):
                self.ui.text_center(
                    16,
                    "{:.0f}°C".format(f.temp),
                    Vect(x, graph_temp.chart_y(f.temp) + 4),
                    BLACK,
                    WHITE,
                )
