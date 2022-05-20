from ulogging import getLogger
logger = getLogger(__name__)

from .. import V, UiFrame, BLACK, WHITE, YELLOW
from cmath import rect, pi


class UiWArrow(UiFrame):
    def draw_wind(self, pos, weather, scale=16, arrow=False):
        def rescale(v):
            return v * scale // 16

        pos = pos + V(0, rescale(30))

        if weather.speed < 2.5:
            self.canvas.fill_rect(V(rescale(-2), rescale(-2)) + pos,
                                  V(rescale(4), rescale(4)),
                                  BLACK)
            return

        r = rescale(30)
        o = pos.x + pos.y * 1j
        d = rect(r, (weather.dir - 90) * pi / 180)

        d2 = o - d

        if weather.speed > 10:
            c = YELLOW
        else:
            c = WHITE

        if weather.speed > 16:
            w = 6
        else:
            w = 3

        self._draw_arrow(weather, d2, o, r, c, w)
        self._draw_arrow(weather, d2, o, r, BLACK, 1)

        if not arrow:
            d1 = o - 0.4 * d
            d = o + d

            def drawWindSpeed(w, c):
                self.canvas.line(V(int(d.real), int(d.imag)), V(int(d1.real), int(d1.imag)), c, w)

                for i in range(int(weather.speed / 2.5)):
                    rr = r - rescale(7) * (i // 2) - rescale(5)
                    l = rescale(15 + 10 * (i % 2))
                    b = rect(rr, (weather.dir - 90) * pi / 180) + o
                    font = rect(l,  (weather.dir - 30) * pi / 180) + b
                    self.canvas.line(V(int(b.real), int(b.imag)), V(int(font.real), int(font.imag)), c, w)

            w = rescale(2) + 1
            drawWindSpeed(w + 1, WHITE)
            drawWindSpeed(w, BLACK)

    def _draw_arrow(self, weather, d2, o, r, c, w):
        if weather.speed < 5:
            r = r * 2 // 3
        elif weather.speed > 7:
            w += 1

        d1 = d2 + rect(r * 2, (weather.dir - 75) * pi / 180)
        self.canvas.line(V(int(d1.real), int(d1.imag)), V(int(d2.real), int(d2.imag)), c, w)
        self.canvas.line(V(int(d1.real), int(d1.imag)), V(int(o.real),  int(o.imag)),  c, w)

        d1 = d2 + rect(r * 2, (weather.dir - 105) * pi / 180)
        self.canvas.line(V(int(d1.real), int(d1.imag)), V(int(d2.real), int(d2.imag)), c, w)
        self.canvas.line(V(int(d1.real), int(d1.imag)), V(int(o.real),  int(o.imag)),  c, w)
