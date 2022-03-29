from ui import UiFrame, Vect, BLACK, YELLOW
from config import temp


class UiOutTemp(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)

    def draw(self, ui, d):
        t = ui.forecast.weather.temp

        if t >= temp.outdoor_high:
            hl = YELLOW
        else:
            hl = None

        ui.text(50, '{:.1f}'.format(t), Vect(21, -5), BLACK, hl, 3)

        bitmap = ui.bitmap(1, 'out')
        ui.canvas.bitmap(Vect(0, 30), bitmap)
