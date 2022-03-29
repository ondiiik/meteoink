import framebuf
import pygame


EPD_WIDTH = 400
EPD_HEIGHT = 300
SIMULATE_REDRAWING = False


class EPD:
    def __init__(self, spi, cs, dc, rst, busy):
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self._factor = 1
        self._frame = 6

        wsize = ((self._frame * 2 + self.width) * self._factor,
                 (self._frame * 2 + self.height) * self._factor)

        self._screen = pygame.display.set_mode(wsize)

        pygame.draw.rect(self._screen,
                         (127, 127, 127),
                         [0, 0, *wsize])
        pygame.display.flip()

        self._clock = pygame.time.Clock()

        pygame.display.set_caption('EPD {} x {}'.format(self.width, self.height))

    def init(self):
        pass

    def display_frame(self, fb_black, fb_yellow):
        self.display_window(fb_black, fb_yellow, 0, 0, EPD_WIDTH, EPD_HEIGHT)

    def _draw_pixel(self, x, y, c):
        pygame.draw.rect(self._screen, c, [(x + self._frame) * self._factor,
                                           (y + self._frame) * self._factor,
                                           self._factor,
                                           self._factor])

    def display_window(self, fb_black, fb_yellow, x, y, w, h):
        progress = ('|', '\\', '-', '/')
        fbb = framebuf.FrameBuffer(fb_black,  EPD_WIDTH, EPD_HEIGHT, framebuf.MONO_HLSB)
        fby = framebuf.FrameBuffer(fb_yellow, EPD_WIDTH, EPD_HEIGHT, framebuf.MONO_HLSB)

        # Draw black frame buffer part
        for i in reversed(range(15)) if SIMULATE_REDRAWING else [0]:
            pygame.display.set_caption('EPD {} x {} - REDRAWING BLACK ({})'.format(self.width, self.height, progress[i % len(progress)]))
            color = ((i * 8, i * 8, i * 8), (255 - i * 8, 255 - i * 8, 255 - i * 8), (0, 0, 0))
            a = i % 2

            for yy in range(EPD_HEIGHT):
                for xx in range(EPD_WIDTH):
                    if (xx >= x) and (yy >= y) and (xx < x + w) and (yy < y + h):
                        self._draw_pixel(xx, yy, color[fbb.pixel(xx, yy) * fby.pixel(xx, yy) + a])

            pygame.display.flip()
            self._clock.tick(4 if i > 7 else 2)

        # Draw yellow frame buffer part
        for i in reversed(range(1, 16)) if SIMULATE_REDRAWING else [1]:
            pygame.display.set_caption('EPD {} x {} - REDRAWING YELLOW ({})'.format(self.width, self.height, progress[i % len(progress)]))
            a = i % 2
            color = ((i * 8, i * 8, i * 8), (255 - i * 8, 255 - i * 8, 0))

            for yy in range(EPD_HEIGHT):
                for xx in range(EPD_WIDTH):
                    c = fby.pixel(xx, yy)
                    if not c and (xx >= x) and (yy >= y) and (xx < x + w) and (yy < y + h):
                        self._draw_pixel(xx, yy, color[a])

            pygame.display.flip()
            self._clock.tick(4 if i > 7 else 2)

        pygame.display.set_caption('EPD {} x {}'.format(self.width, self.height))
