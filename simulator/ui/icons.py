from ui import UiFrame, Vect
from forecast import id2icon
from micropython import const


class UiIcons(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)

    def draw(self, ui, d):
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

            ui.canvas.bitmap(Vect(xx, i % rows_cnt * h_icons), bitmap)
