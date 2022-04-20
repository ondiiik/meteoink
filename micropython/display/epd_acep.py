# MicroPython Waveshare 5.65" 7 color e-paper display driver
# Based on https://github.com/mcauser/micropython-waveshare-epaper
#
# MIT License
# Copyright (c) 2017 Waveshare
# Copyright (c) 2018 Mike Causer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from ulogging import getLogger
logger = getLogger(__name__)

from micropython import const
from time import sleep_ms
from struct import pack
from machine import SPI, Pin
from setup import pins


ACEP_PANEL_SETTING = const(0x00)
ACEP_POWER_SETTING = const(0x01)
ACEP_POWER_OFF = const(0x02)
ACEP_POWER_OFF_SEQUENCE = const(0x03)
ACEP_POWER_ON = const(0x04)
ACEP_BOOSTER_SOFT_START = const(0x06)
ACEP_DEEP_SLEEP = const(0x07)
ACEP_DTM = const(0x10)
ACEP_DISPLAY_REFRESH = const(0x12)
ACEP_PLL = const(0x30)
ACEP_TSE = const(0x40)
ACEP_CDI = const(0x50)
ACEP_TCON = const(0x60)
ACEP_RESOLUTION = const(0x61)
ACEP_PWS = const(0xE3)

_cleanup = b''


class EPD:
    @micropython.native
    def __init__(self):
        logger.info("Building display:")
        self.width = 600
        self.height = 448

        self._spi = SPI(1)
        self._spi.init(baudrate=2000000,
                       polarity=0,
                       phase=0,
                       sck=Pin(pins.SCK),
                       mosi=Pin(pins.MOSI),
                       miso=Pin(pins.MISO))
        logger.info("\tSPI - [ OK ]")

        self._cs = Pin(pins.CS)
        self._dc = Pin(pins.DC)
        self._rst = Pin(pins.RST)
        self._busy = Pin(pins.BUSY)
        self._resolution = pack('!HH', self.width, self.height)

        self._cs.init(self._cs.OUT,  value=1)
        self._dc.init(self._dc.OUT,  value=0)
        self._rst.init(self._rst.OUT, value=0)
        self._busy.init(self._busy.IN)

        self._initialized = False

    @micropython.native
    def display_frame(self, buf):
        self._init()
        self._flush_frame(buf)
        self._sleep()

    @micropython.native
    def deghost(self, buf):
        self._init()
        for i in range(len(buf)):
            buf[i] = 0x77
        self._flush_frame(buf)

    @micropython.native
    def _cmd(self, command, data=None):
        self._dc(0)
        self._cs(0)
        self._spi.write(bytearray([command]))
        self._cs(1)
        if data is not None:
            self._data(data)

    @micropython.native
    def _data(self, data):
        self._dc(1)
        self._cs(0)
        self._spi.write(data)
        self._cs(1)

    @micropython.native
    def _flush_frame(self, buf):
        self._cmd(ACEP_RESOLUTION, self._resolution)
        self._cmd(ACEP_DTM, buf)
        self._cmd(ACEP_POWER_ON)
        self._wait4ready()
        self._cmd(ACEP_DISPLAY_REFRESH)
        self._wait4ready()
        self._cmd(ACEP_POWER_OFF)
        sleep_ms(500)

    @micropython.native
    def _reset(self):
        self._rst(True)
        sleep_ms(10)
        self._rst(False)
        sleep_ms(10)
        self._rst(True)
        sleep_ms(200)
        self._wait4ready()

    @micropython.native
    def _init(self):
        if self._initialized:
            return

        self._reset()
        self._wait4ready()

        sleep_ms(10)
        self._cmd(ACEP_PANEL_SETTING, b'\xEF\x08')
        self._cmd(ACEP_POWER_SETTING, b'\x37\x00\x23\x23')
        self._cmd(ACEP_POWER_OFF_SEQUENCE, b'\x00')
        self._cmd(ACEP_BOOSTER_SOFT_START, b'\xC7\xC7\x1D')
        self._cmd(ACEP_PLL, b'\x3C')
        self._cmd(ACEP_TSE, b'\x00')
        self._cmd(ACEP_CDI, b'\x37')
        self._cmd(ACEP_TCON, b'\x22')
        self._cmd(ACEP_RESOLUTION, self._resolution)
        self._cmd(ACEP_PWS, b'\xAA')
        sleep_ms(100)

    @micropython.native
    def _sleep(self):
        self._cmd(ACEP_POWER_OFF)
        self._wait4ready()
        self._cmd(ACEP_DEEP_SLEEP, b'\xA5')

    @micropython.native
    def _wait4ready(self):
        for i in range(2000):
            if self._busy.value():
                return
            sleep_ms(10)

        raise RuntimeError('EPD Timeout')
