from ulogging import getLogger
from ui import UiFrame, Vect, ONE, TWO
from display.epd import BLACK, WHITE, GRAY

logger = getLogger(__name__)


class UiRain(UiFrame):
    def draw(self):
        # Pre-calculates some range values and draw icons bar
        block = self.ui.block

        self.canvas.hline(Vect(0, self.dim.y - 2), self.dim.x - 1, BLACK)

        for x, fl, f, fr in self.ui.forecast_tripples():
            # Draw rain chart
            p = max(f.rain, f.snow)

            if f.rain > 0 or f.snow > 0:
                r = int(p * 12)
                q = self.dim.y // 4
                for h in (q, q * 2, q * 3):
                    if r > h:
                        r = h + (r - h) // 2
                v = Vect(x - int(block // 2) + 1, self.dim.y - r - 1)
                d = Vect(int(block) - 2, r)

                if f.rain > 0:
                    self.canvas.fill_rect(v, d, GRAY)
                else:
                    self.canvas.fill_rect(v, d, WHITE)
                    self.canvas.rect(v - ONE, d - TWO, BLACK)
                self.canvas.rect(v, d, BLACK)

            # Type rain text
            if (max(fl.rain, fl.snow) < p) and (p > max(fr.rain, fr.snow)):
                self.ui.text_center(25, "%.1f" % p, Vect(x, self.dim.y - 2), BLACK)
