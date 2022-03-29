from ui import UiFrame, Vect, BLACK, YELLOW
from config import temp


class UiInTemp(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)

    def draw(self, ui, d):
        t = ui.forecast.home.temp
        hl = None

        if not None == t:
            if t >= temp.indoor_high:
                hl = YELLOW

            t = '{:.1f}'.format(t)
        else:
            t = '--'

        ui.text(50, t, Vect(21, -5), BLACK, hl, 3)

        bitmap = ui.bitmap(1, 'in')
        ui.canvas.bitmap(Vect(0, 30), bitmap)
