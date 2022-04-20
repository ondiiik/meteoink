# MicroPython Waveshare 4.2" Black/White/Red GDEW042Z15 e-paper display driver
# https://github.com/mcauser/micropython-waveshare-epaper
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

import micropython
from struct import pack
from time import sleep_ms
from machine import SPI, Pin
from setup import pins
from .base import BLACK, WHITE, YELLOW

# also works for black/white/yellow GDEW042C37?

# Display commands


def _convert(in_buf, lut):
    l = len(in_buf) // 4
    out_buf = bytearray(l)
    i_s = 0
    for i_d in range(l):
        b = 0
        for i in range(4):
            b <<= 2
            b |= lut.get(in_buf[i_s], 0)
            i_s += 1
        out_buf[i_d] = b
    return out_buf


class EPD:
    @micropython.native
    def __init__(self):
        logger.info("Building display:")
        self.width = 400
        self.height = 300

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

    @micropython.native
    def display_frame(self, buf):
        self._init()

        black = _convert(buf, {(WHITE << 4) | WHITE: 0b11,
                               (WHITE << 4) | YELLOW: 0b10,
                               (WHITE << 4) | BLACK: 0b10,
                               (BLACK << 4) | WHITE: 0b01,
                               (YELLOW << 4) | WHITE: 0b01,
                               (BLACK << 4) | BLACK: 0b00,
                               (BLACK << 4) | YELLOW: 0b00,
                               (YELLOW << 4) | BLACK: 0b00,
                               (YELLOW << 4) | YELLOW: 0b00})
        yellow = _convert(buf, {(WHITE << 4) | WHITE: 0b11,
                                (WHITE << 4) | YELLOW: 0b10,
                                (WHITE << 4) | BLACK: 0b11,
                                (BLACK << 4) | WHITE: 0b11,
                                (YELLOW << 4) | WHITE: 0b01,
                                (BLACK << 4) | BLACK: 0b11,
                                (BLACK << 4) | YELLOW: 0b10,
                                (YELLOW << 4) | BLACK: 0b01,
                                (YELLOW << 4) | YELLOW: 0b00})

        self._flush_frame(black, yellow)

        self._cmd(0x12)
        self._wait4ready()
        self._sleep()

    @micropython.native
    def deghost(self, buf):
        pass

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
    def _flush_frame(self, black, yellow):
        self._cmd(0x10, black)
        self._cmd(0x13, yellow)

    @micropython.native
    def _reset(self):
        self._rst(0)
        sleep_ms(200)
        self._rst(1)
        sleep_ms(200)

    @micropython.native
    def _init(self):
        self._reset()
        self._cmd(0x06, b'\x17\x17\x17')   # Boost start ...
        self._cmd(0x00, b'\x0F')           # LUT from OTP Pixel with B/W/Y
        self._cmd(0x61, self._resolution)  # Resolution setting
        self._cmd(0x50, b'\xF7')           # Data setting: WBmode:VBDF 17|D7 VBDW 97 VBDB 57, WBRmode:VBDF F7 VBDW 77 VBDB 37  VBDR B7
        self._cmd(0x04)                    # Power ON
        self._wait4ready()

    @micropython.native
    def _sleep(self):
        self._cmd(0x02)
        self._wait4ready()
        self._cmd(0x07, b'\xA5')

    @micropython.native
    def _wait4ready(self):
        for i in range(3000):
            if self._busy.value():
                return
            sleep_ms(10)

        raise RuntimeError('EPD Timeout')
