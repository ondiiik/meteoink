from framebuf import FrameBuffer, GS4_HMSB
from machine import deepsleep, reset, reset_cause, HARD_RESET
from ulogging import getLogger
from ustruct import pack, unpack
import micropython
import pygame

logger = getLogger(__name__)

ALPHA = 1
BLACK = 0
GRAY = 13
WHITE = 15


class Epd47:
    WIDTH = 960
    HEIGHT = 540

    def __init__(self):
        def _iter():
            for i in range(self.WIDTH * self.HEIGHT // 2):
                yield 255

        self._fb = bytearray(_iter())

    def fb(self):
        return self._fb

    def on(self):
        logger.info("EPD ON")

    def off(self):
        logger.info("EPD OFF")

    def power_off(self):
        logger.info("EPD POWER OFF")

    def clear(self):
        logger.info("EPD Clear")

    def flush(self):
        logger.info("EPD Draw area {}x{}:{}+{}".format(0, 0, self.WIDTH, self.HEIGHT))

        fb = FrameBuffer(self._fb, self.WIDTH, self.HEIGHT, GS4_HMSB)

        for yy in range(self.HEIGHT):
            for xx in range(self.WIDTH):
                _draw_pixel(xx, yy, fb.pixel(xx, yy) * 8)

        pygame.display.flip()
        _clock.tick(4)


class EPD:
    epd = Epd47()

    @micropython.native
    def __init__(self):
        if reset_cause() == HARD_RESET:
            t = self._reload_frame()
            logger.debug(f"EPD47: Deepsleep {t / 1000} seconds")
            deepsleep(t)
        else:
            logger.debug("EPD47 - WiFi mode")
            self.width = Epd47.WIDTH
            self.height = Epd47.HEIGHT
            self._fb = bytearray(self.width * self.height // 2)

    @micropython.native
    def init(self):
        ...

    @micropython.native
    def fb(self):
        return self._fb

    @micropython.native
    def display_frame(self):
        ...

    @micropython.native
    def display_frame_now(self):
        with open("bitmaps/fb.bin", "wb") as f:
            f.write(pack("I", 1))
            f.write(self._fb)
        self._reload_frame()

    @micropython.native
    def deghost(self):
        ...

    @micropython.native
    def deepsleep(self, t):
        with open("bitmaps/fb.bin", "wb") as f:
            f.write(pack("I", t))
            f.write(self._fb)
        reset()

    @micropython.native
    def _reload_frame(self):
        logger.debug("EPD47 - repaint mode")
        try:
            with open("bitmaps/fb.bin", "rb") as f:
                t = unpack("I", f.read(4))[0]
                f.readinto(self.epd.fb())
        except:
            logger.warning("Nothing to repaint - restarting")
            deepsleep(1)

        logger.debug("EPD47: Power ON")
        self.epd.on()
        logger.debug("EPD47: Clear")
        self.epd.clear()
        logger.debug("EPD47: Flush")
        self.epd.flush()
        logger.debug("EPD47: Power OFF")
        self.epd.power_off()

        return t


_factor = 1
_frame = 6

wsize = ((_frame * 2 + Epd47.WIDTH) * _factor, (_frame * 2 + Epd47.HEIGHT) * _factor)

_screen = pygame.display.set_mode(wsize)

pygame.draw.rect(_screen, (127, 127, 127), [0, 0, *wsize])
pygame.display.flip()

_clock = pygame.time.Clock()

pygame.display.set_caption("EPD {} x {}".format(Epd47.WIDTH, Epd47.HEIGHT))


def _draw_pixel(x, y, c):
    pygame.draw.rect(
        _screen,
        c + c * 256 + c * 65536,
        [(x + _frame) * _factor, (y + _frame) * _factor, _factor, _factor],
    )


BLACK_ON_WHITE = 0
