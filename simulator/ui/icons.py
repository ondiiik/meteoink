from ui import UiFrame, Vect as V
from micropython import const


class UiIcons(UiFrame):
    def draw(self, ui):
        # Pre-calculates some range values and draw icons bar
        rows_cnt = const(2)
        forecast = ui.forecast.forecast
        cnt = len(forecast)
        h_icons = self.dim.y // rows_cnt
        icon = {}

        for i in range(cnt):
            xx = ui.canvas.dim.x * i // (cnt + 1)
            id = forecast[i].icon

            try:
                bitmap = icon[id]
            except KeyError:
                bitmap = ui.bitmap(4, id)
                icon[id] = bitmap

            ui.canvas.bitmap(V(xx, i % rows_cnt * h_icons), bitmap)
