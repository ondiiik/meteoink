from ulogging import getLogger
logger = getLogger(__name__)

from .. import Vect as V, UiFrame, BLACK, WHITE, YELLOW
from cmath import rect, pi


class UiWArrow(UiFrame):
    def draw_wind(self, pos, weather, scale=16, arrow=False):
        speed = weather.speed
        direction = weather.dir

        def rescale(v):
            return v * scale // 16

        pos = pos + V(0, rescale(30))

        if speed < 2.5:
            self.canvas.fill_rect(V(rescale(-2), rescale(-2)) + pos,
                                  V(rescale(4), rescale(4)),
                                  BLACK)
            return

        r = rescale(30)
        o = pos.x + pos.y * 1j
        d = rect(r, (direction - 90) * pi / 180)

        d2 = o - d

        if speed > 10:
            c = YELLOW
        else:
            c = WHITE

        if speed > 16:
            w = 6
        else:
            w = 3

        self._draw_arrow(speed, direction, d2, o, r, c, w)
        self._draw_arrow(speed, direction, d2, o, r, BLACK, 1)

        if not arrow:
            d1 = o - 0.4 * d
            d = o + d

            def drawWindSpeed(w, c):
                self.canvas.line(V(int(d.real), int(d.imag)), V(int(d1.real), int(d1.imag)), c, w)

                for i in range(int(speed / 2.5)):
                    rr = r - rescale(7) * (i // 2) - rescale(5)
                    l = rescale(15 + 10 * (i % 2))
                    b = rect(rr, (direction - 90) * pi / 180) + o
                    e = rect(l,  (direction - 30) * pi / 180) + b
                    self.canvas.line(V(int(b.real), int(b.imag)), V(int(e.real), int(e.imag)), c, w)

            w = rescale(2) + 1
            drawWindSpeed(w + 1, WHITE)
            drawWindSpeed(w, BLACK)

    def _draw_arrow(self, speed, direction, d2, o, r, c, w):
        if speed < 5:
            r = r * 2 // 3
        elif speed > 7:
            w += 1

        d1 = d2 + rect(r * 2, (direction - 75) * pi / 180)
        self.canvas.line(V(int(d1.real), int(d1.imag)), V(int(d2.real), int(d2.imag)), c, w)
        self.canvas.line(V(int(d1.real), int(d1.imag)), V(int(o.real),  int(o.imag)),  c, w)

        d1 = d2 + rect(r * 2, (direction - 105) * pi / 180)
        self.canvas.line(V(int(d1.real), int(d1.imag)), V(int(d2.real), int(d2.imag)), c, w)
        self.canvas.line(V(int(d1.real), int(d1.imag)), V(int(o.real),  int(o.imag)),  c, w)
