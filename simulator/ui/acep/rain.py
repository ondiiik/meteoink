from ulogging import getLogger
logger = getLogger(__name__)

from .. import UiFrame, V, BLACK, WHITE, BLUE, GREEN, YELLOW, RED


class UiRain(UiFrame):
    def draw(self):
        block = self.ui.block

        self.canvas.hline(V(0, self.height - 1), self.dim.x - 1, BLACK)
        crv = V(3, 3)
        crd = crv + V(crv.x, 0)
        q = self.height // 4
        q2 = q * 2
        q3 = q * 3

        def gen():
            for x, fl, f, fr in self.ui.forecast_tripples():
                p = max(f.rain, f.snow)

                if p:
                    r = int(p * 16)
                    for h in (q, q2, q3):
                        if r > h:
                            r = h + (r - h) // 2
                    v, d = V(x - int(block // 2) + 1, self.height - r - 1), V(int(block) - 2, r)
                else:
                    v, d = None, None

                if (max(fl.rain, fl.snow) < p) and (p > max(fr.rain, fr.snow)):
                    t = f'{p:.1f}', V(x, self.height - 2)
                else:
                    t = None

                yield v, d, t, f.rain

        gen = list(gen())

        for v, d, t, r in gen:
            if v is not None:
                self.canvas.trect(v - crv, d + crd, YELLOW)

        for v, d, t, r in gen:
            if v is not None:
                if r:
                    self.canvas.fill_rect(v, d, RED)
                else:
                    self.canvas.fill_rect(v, d, WHITE)
                    self.canvas.trect(v, d, BLUE)
                    self.canvas.rect(v, d, BLUE)

        for v, d, t, r in gen:
            if t:
                self.ui.text_center(16, t[0], t[1], BLACK, WHITE)
