# Display panel connected through SPI (ESP32)
#
# Thin adapter between meteostation and `ueink` display driver.
from ulogging import getLogger

logger = getLogger(__name__)

from machine import SPI, Pin, deepsleep
from config import hw


class Panel:
    DRIVER = None  # ueink display driver class
    ROTATED = False  # Display is mounted rotated by 90 degrees (portrait)
    DEGHOST = False  # Clean display before each flush

    def __init__(self):
        logger.info("Building display:")
        p = hw["pins"]

        spi = SPI(
            1,
            baudrate=2000000,
            polarity=0,
            phase=0,
            sck=Pin(p["sck"]),
            mosi=Pin(p["mosi"]),
            miso=Pin(p["miso"]),
        )

        self._epd = self.DRIVER(
            spi=spi,
            cs=Pin(p["cs"]),
            dc=Pin(p["dc"]),
            rst=Pin(p["rst"]),
            busy=Pin(p["busy"]),
        )
        self.width, self.height = self.DRIVER.dim

    def fb(self):
        # Native (not rotated) GS4_HMSB frame buffer of display
        return self._epd.buf

    def display_frame(self):
        self._epd.flush()

    def deghost(self):
        if self.DEGHOST:
            self._epd.clean()

    def deepsleep(self, t):
        if t:
            deepsleep(t)
        else:
            deepsleep()
