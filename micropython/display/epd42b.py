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

# also works for black/white/yellow GDEW042C37?


# Display commands
class EPD:
    def __init__(self, spi, cs, dc, rst, busy):
        self.spi  = spi
        self.cs   = cs
        self.dc   = dc
        self.rst  = rst
        self.busy = busy
        
        self.cs.init(  self.cs.OUT,  value=1)
        self.dc.init(  self.dc.OUT,  value=0)
        self.rst.init( self.rst.OUT, value=0)
        self.busy.init(self.busy.IN)
        
        self.width  = 400
        self.height = 300

    def _command(self, command, data=None):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)
        if data is not None:
            self._data(data)

    def _data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    # draw the current frame memory
    def _flush_frame(self, fb_black, fb_yellow):
        self._command(0x10, fb_black)   # Black buffer transmission
        self._command(0x13, fb_yellow)  # Yellow buffer transmission

    def _set_window(self, x, y, w, h):
        from struct import pack
        xe  = (x + w - 1) | 0x0007; # Byte boundary inclusive (last byte)
        ye  =  y + h - 1;
        x  &= 0xFFF8;               # Byte boundary
        xe |= 0x0007
        self._command(0x90, pack('!HHHH', x, xe, y, ye))  # Resolution setting
        #self._command(0x90, bytes([x //  256,  # Resolution setting
        #                           x %   256,
        #                           xe // 256,
        #                           xe %  256,
        #                           y //  256,
        #                           y %   256,
        #                           ye // 256,
        #                           ye %  256]))
        #self._command(0x01) # Distortion on full right half
        self._command(0x00) # Distortion on right half

    def _reset(self):
        from time import sleep_ms
        self.rst(0)
        sleep_ms(200)
        self.rst(1)
        sleep_ms(200)

    def _init(self):
        from struct import pack
        self._reset()
        self._command(0x06, b'\x17\x17\x17')                      # Boost start ...
        self._command(0x00, b'\x0F')                              # LUT from OTP Pixel with B/W/Y
        self._command(0x61, pack('!HH', self.width, self.height)) # Resolution setting
        self._command(0x50, b'\xF7')                              # Data setting: WBmode:VBDF 17|D7 VBDW 97 VBDB 57, WBRmode:VBDF F7 VBDW 77 VBDB 37  VBDR B7
        self._command(0x04)                                       # Power ON
        self._wait_until_idle()

    # to wake call _init()
    def _sleep(self):
        self._command(0x02)          # Power off display
        self._wait_until_idle()
        self._command(0x07, b'\xA5') # Deep sleep

    def _wait_until_idle(self):
        from time import sleep_ms
        while self.busy.value() == 0:
            sleep_ms(100)

    # draw the current frame memory
    def display_frame(self, fb_black, fb_yellow):
        self._init()
        self._flush_frame(fb_black, fb_yellow)  # Load data into display
        self._command(0x12)                     # Refresh display
        self._wait_until_idle()
        self._sleep()                           # Suspend display

    # draw just part of display
    def display_window(self, fb_black, fb_yellow, x, y, w, h):
        x  -= x % 8
        w  -= x % 8
        x1  = 0 if x < 0 else x
        y1  = 0 if y < 0 else y
        w1  = x + (w if w < self.width  else (self.width  - x))
        h1  = y + (h if h < self.height else (self.height - y))
        w1 -= x1 - x;
        h1 -= y1 - y;
        
        self._init()
        self._flush_frame(fb_black, fb_yellow) # Load data into display
        self._command(0x91)                    # Partial data refresh mode ON
        self._set_window(x, y, w, h)           # Set partial ram area
        self._command(0x12)                    # Refresh display
        self._command(0x92)                    # Partial data refresh mode OFF
        self._sleep()                          # Suspend display
