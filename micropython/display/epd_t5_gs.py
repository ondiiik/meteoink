from epd47 import Epd47
from machine import deepsleep, reset, reset_cause, HARD_RESET
from ulogging import getLogger
from ustruct import pack, unpack

logger = getLogger(__name__)

ALPHA = const(1)
BLACK = const(0)
GRAY = const(13)
WHITE = const(15)


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
