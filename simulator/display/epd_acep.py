from framebuf import FrameBuffer, GS4_HMSB
from itertools import product
from machine import deepsleep
import pygame


EPD_WIDTH = 600
EPD_HEIGHT = 448

ALPHA = 7
BLACK = 0
BLUE = 3
GREEN = 2
ORANGE = 6
RED = 4
WHITE = 1
YELLOW = 5


colors = (
    (43, 46, 62),
    (227, 227, 227),
    (73, 110, 86),
    (56, 67, 104),
    (170, 82, 81),
    (222, 207, 105),
    (197, 102, 86),
    (183, 138, 126),
)


class EPD:
    def __init__(self):
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self._factor = 1
        self._frame = 6

        self._fb = bytearray((self.width * self.height + 1) // 2)

        wsize = (
            (self._frame * 2 + self.height) * self._factor,
            (self._frame * 2 + self.width) * self._factor,
        )

        self._screen = pygame.display.set_mode(wsize)

        pygame.draw.rect(self._screen, (127, 127, 127), [0, 0, *wsize])
        pygame.display.flip()

        self._clock = pygame.time.Clock()

        pygame.display.set_caption("EPD {} x {} - ACEP".format(self.width, self.height))

    def init(self):
        ...

    def fb(self):
        return self._fb

    def display_frame(self):
        fb = FrameBuffer(self._fb, EPD_WIDTH, EPD_HEIGHT, GS4_HMSB)

        for y, x in product(range(EPD_HEIGHT), range(EPD_WIDTH)):
            self._draw_pixel(x, y, colors[fb.pixel(x, y) & 7])

        pygame.display.flip()
        self._clock.tick(2)

    def deghost(self):
        ...

    def deepsleep(self, t):
        deepsleep(t)

    def _draw_pixel(self, x, y, c):
        pygame.draw.rect(
            self._screen,
            c,
            [
                (self.height - y + self._frame) * self._factor,
                (x + self._frame) * self._factor,
                self._factor,
                self._factor,
            ],
        )
