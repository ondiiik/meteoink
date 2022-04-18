import pygame
from itertools import product
from framebuf import FrameBuffer, GS4_HMSB


EPD_WIDTH = 600
EPD_HEIGHT = 480
SIMULATE_REDRAWING = False

colors = ((43,  46,  62),
          (227, 227, 227),
          (73,  110, 86),
          (56,  67,  104),
          (170, 82,  81),
          (222, 207, 105),
          (197, 102, 86),
          (183, 138, 126))


class EPD:
    def __init__(self, spi, cs, dc, rst, busy):
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self._factor = 2
        self._frame = 6

        wsize = ((self._frame * 2 + self.width) * self._factor,
                 (self._frame * 2 + self.height) * self._factor)

        self._screen = pygame.display.set_mode(wsize)

        pygame.draw.rect(self._screen,
                         (127, 127, 127),
                         [0, 0, *wsize])
        pygame.display.flip()

        self._clock = pygame.time.Clock()

        pygame.display.set_caption('EPD {} x {} - ACEP'.format(self.width, self.height))

    def init(self):
        pass

    def _draw_pixel(self, x, y, c):
        pygame.draw.rect(self._screen, c, [(x + self._frame) * self._factor,
                                           (y + self._frame) * self._factor,
                                           self._factor,
                                           self._factor])

    def display_frame(self, buf):
        fb = FrameBuffer(buf, EPD_WIDTH, EPD_HEIGHT, GS4_HMSB)

        for y, x in product(range(EPD_HEIGHT), range(EPD_WIDTH)):
            self._draw_pixel(x, y, colors[fb.pixel(x, y) & 7])

        pygame.display.flip()
        self._clock.tick(2)
