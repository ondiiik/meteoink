from ui import UiFrame, Vect as V, BLACK, WHITE, YELLOW


class UiVBat(UiFrame):
    def draw(self, ui, volt):
        from config import vbat

        w = self.dim.x
        h = self.dim.y
        p = min(max((volt - vbat.low_voltage) / (4.2 - vbat.low_voltage), 0), 1)
        l = int(p * w)

        if p < 0.2:
            ui.canvas.fill_rect(V(-6, -13), V(w + 16, h + 18), YELLOW)
        else:
            ui.canvas.fill_rect(V(-4, -11), V(w + 9, h + 14), WHITE)

        ui.canvas.rect(V(0, 0), V(w + 3, h))
        ui.canvas.fill_rect(V(-3, h // 2 - 2), V(3, 5))
        ui.canvas.fill_rect(V(1 + w - l, 2), V(l, h - 4))

        if vbat.show_voltage:
            ui.text_center(10, '{:.2}V'.format(volt), V(w // 2 + 2, -12))
        else:
            ui.text_center(10, '{:.0%}'.format(p), V(w // 2 + 2, -12))

        if (volt < vbat.low_voltage):
            ui.canvas.line(V(0, 0), self.dim, YELLOW, w=6)
            ui.canvas.line(V(0, 0), self.dim, BLACK,  w=2)
