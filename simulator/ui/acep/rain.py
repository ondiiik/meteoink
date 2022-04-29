from ulogging import getLogger
logger = getLogger(__name__)

from .. import UiFrame, V, BLACK, WHITE, BLUE, GREEN


class UiRain(UiFrame):
    def draw(self):
        # Pre-calculates some range values and draw icons bar
        block = self.ui.block

        self.canvas.hline(V(0, self.dim.y - 1), self.dim.x - 1, BLACK)
        coronv = V(6, 6)
        corond = coronv + V(coronv.x, 0)

        for x, fl, f, fr in self.ui.forecast_tripples():
            # Draw rain chart
            p = max(f.rain, f.snow)

            if f.rain > 0 or f.snow > 0:
                r = int(p * 12)
                q = self.dim.y // 4
                for h in (q, q * 2, q * 3):
                    if r > h:
                        r = h + (r - h) // 2
                v = V(x - int(block // 2) + 1, self.dim.y - r - 1)
                d = V(int(block) - 2, r)

                self.canvas.trect(v - coronv, d + corond, BLUE)
                if f.rain > 0:
                    self.canvas.fill_rect(v, d, BLUE)
                else:
                    self.canvas.trect(v, d, GREEN)
                    self.canvas.rect(v, d, BLUE)

            # Type rain text
            if (max(fl.rain, fl.snow) < p) and (p > max(fr.rain, fr.snow)):
                self.ui.text_center(16, '%.1f' % p, V(x, self.dim.y - 2), BLACK, WHITE)
