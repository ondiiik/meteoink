import                    framebuf
from   config      import pins
from   micropython import const
import micropython


WHITE  = const(3)
BLACK  = const(2)
YELLOW = const(1)


class Vect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    @property
    def square(self):
        return self.x * self.y
    
    def __add__(self, v):
        return Vect(self.x + v.x, self.y + v.y)
    
    def __sub__(self, v):
        return Vect(self.x - v.x, self.y - v.y)
    
    def __mul__(self, v):
        return Vect(self.x * v, self.y * v)
    
    def __div__(self, v):
        return Vect(self.x // v, self.y // v)



class Bitmap:
    def __init__(self, file_name, no_load = False):
        f        = open(file_name, 'rb')
        hdr      = f.read(2)
        self.dim = Vect(int(hdr[1]), int(hdr[0]))
        
        if no_load:
            return
        
        self.buf_width = ((self.dim.x + 7) // 8) * 8
        cnt            = (self.buf_width * self.dim.y) // 8
        self.buf       = (bytearray(f.read(cnt)),
                          bytearray(f.read(cnt)),
                          bytearray(f.read(cnt)),
                          bytearray(f.read(cnt)))
        f.close()
        self.fb        = (framebuf.FrameBuffer(self.buf[0], self.buf_width, self.dim.y, framebuf.MONO_HLSB),
                          framebuf.FrameBuffer(self.buf[1], self.buf_width, self.dim.y, framebuf.MONO_HLSB),
                          framebuf.FrameBuffer(self.buf[2], self.buf_width, self.dim.y, framebuf.MONO_HLSB),
                          framebuf.FrameBuffer(self.buf[3], self.buf_width, self.dim.y, framebuf.MONO_HLSB))
    
    def inverted(self, idx = 0):
        l   = len(self.buf[idx])
        buf = bytearray(b'\x00' * l)
        
        for i in range(l):
            buf[i] = (~self.buf[idx][i]) & 0xFF
        
        return framebuf.FrameBuffer(buf, self.buf_width, self.dim.y, framebuf.MONO_HLSB)


class Fb:
    def __init__(self, color, epd):
        print("\tFB%d - [ OK ]" % color)
        
        self.buf    = bytearray((epd.width * epd.height + 7) // 8)
        self.canvas = framebuf.FrameBuffer(self.buf, epd.width, epd.height, framebuf.MONO_HLSB)
        self.epd    = epd
        self._bit   = 1 if color == YELLOW else 0
    
    
    @micropython.native
    def fill(self, c):
        self.canvas.fill((c >> self._bit) & 1)
    
    
    @micropython.native
    def htline(self, x, y, w, c):
        a      = 0 if c == BLACK else 1
        c      = (c >> self._bit) & 1
        canvas = self.canvas
        
        for xx in range (x, x + w):
            if (xx + y + a) % 2 == 0:
                canvas.pixel(xx, y, c)
    
    
    @micropython.native
    def hline(self, x, y, w, c):
        self.canvas.hline(x, y, w, (c >> self._bit) & 1)
    
    
    @micropython.native
    def vtline(self, x, y, h, c):
        c      = (c >> self._bit) & 1
        canvas = self.canvas
        
        for yy in range (y, y + h):
            if (yy + x + 1) % 2 == 0:
                canvas.pixel(x, yy, c)
    
    
    @micropython.native
    def vline(self, x, y, h, c):
        self.canvas.vline(x, y, h, (c >> self._bit) & 1)
    
    
    @micropython.native
    def line(self, x1, y1, x2, y2, c):
        self.canvas.line(x1, y1, x2, y2, (c >> self._bit) & 1)
    
    
    @micropython.native
    def rect(self, x, y, w, h, c):
        self.canvas.rect(x, y, w, h, (c >> self._bit) & 1)
    
    
    @micropython.native
    def trect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            self.htline(x,yy, w, c)
    
    
    @micropython.native
    def fill_rect(self, x, y, w, h, c):
        self.canvas.fill_rect(x, y, w, h, (c >> self._bit) & 1)
    
    
    @micropython.native
    def text(self, s, x, y, c):
        self.canvas.text(s, x, y, (c >> self._bit) & 1)



class Canvas:
    def __init__(self):
        print("Building EPD:")
        # Load modules and set constants
        from display import epd42b as epaper
        from machine import SPI, Pin
        
        # Initializes SPI
        spi = SPI(1)
        spi.init(baudrate = 2000000,
                 polarity = 0,
                 phase    = 0,
                 sck      = Pin(pins.SCK),
                 mosi     = Pin(pins.MOSI),
                 miso     = Pin(pins.MISO))
        cs                = Pin(pins.CS)
        dc                = Pin(pins.DC)
        rst               = Pin(pins.RST)
        busy              = Pin(pins.BUSY)
        print("\tSPI - [ OK ]")
        
        # Create EPD epaper driver
        epd      = epaper.EPD(spi, cs, dc, rst, busy)
        self.dim = Vect(epd.width, epd.height)
        self.ofs = Vect(0, 0)
        print("\tEPD - [ OK ]")
        
        self.fb = ( Fb(BLACK, epd), Fb(YELLOW, epd) )
    
    
    @micropython.native
    def clear(self):
        self.fill(WHITE)
    
    
    @micropython.native
    def fill(self, c):
        for fb in self.fb:
            fb.fill(c)
    
    
    @micropython.native
    def flush(self, sector = None):
        if sector is None:
            self.fb[0].epd.display_frame(self.fb[0].buf, self.fb[1].buf)
        else:
            self.fb[0].epd.display_window(self.fb[0].buf, self.fb[1].buf, sector[0], sector[1], sector[2], sector[3])
    
    
    @micropython.native
    def hline(self, v, w, c = BLACK):
        v += self.ofs
        for fb in self.fb:
            fb.hline(v.x, v.y, w, c)
    
    
    @micropython.native
    def htline(self, v, w, c = BLACK):
        v += self.ofs
        for fb in self.fb:
            fb.htline(v.x, v.y, w, c)
    
    
    @micropython.native
    def vtline(self, v, h, c = BLACK):
        v += self.ofs
        for fb in self.fb:
            fb.vtline(v.x, v.y, h, c)
    
    
    @micropython.native
    def vline(self, v, h, c = BLACK):
        v += self.ofs
        for fb in self.fb:
            fb.vline(v.x, v.y, h, c)
    
    
    @micropython.native
    def line(self, v1, v2, c = BLACK, w = 1):
        l = self.line
        
        if w == 2:
            for a in (Vect(1, 0), Vect(0, 1), Vect(1, 1)):
                l(v1 + a, v2 + a, c)
        elif w > 2:
            for a in (Vect(1, 0), Vect(0, 1), Vect(1, 1), Vect(1, -1)):
                for i in range(w // 2):
                    l(v1 + a * (i + 1), v2 + a * (i + 1), c)
                    l(v1 - a * (i + 1), v2 - a * (i + 1), c)
        
        v1 += self.ofs
        v2 += self.ofs
        
        for fb in self.fb:
            fb.line(v1.x, v1.y, v2.x, v2.y, c)
    
    
    @micropython.native
    def rect(self, v, d, c = BLACK):
        v += self.ofs
        for fb in self.fb:
            fb.rect(v.x, v.y, d.x, d.y, c)
    
    
    @micropython.native
    def trect(self, v, d, c = BLACK):
        v += self.ofs
        for fb in self.fb:
            fb.trect(v.x, v.y, d.x, d.y, c)
    
    
    @micropython.native
    def fill_rect(self, v, d, c = BLACK):
        v += self.ofs
        for fb in self.fb:
            fb.fill_rect(v.x, v.y, d.x, d.y, c)
    
    
    @micropython.native
    def text(self, s, v, c = BLACK):
        v += self.ofs
        for fb in self.fb:
            fb.text(s, v.x, v.y, c)
    
    
    @micropython.native
    def bitmap(self, v, bitmap, color = None):
        v  += self.ofs
        fb  = self.fb
        
        if color is None:
            fb[0].canvas.blit(bitmap.fb[0], v.x, v.y, 1)
            fb[0].canvas.blit(bitmap.fb[1], v.x, v.y, 0)
            fb[1].canvas.blit(bitmap.fb[2], v.x, v.y, 1)
            fb[1].canvas.blit(bitmap.fb[3], v.x, v.y, 0)
        else:
            if   color == BLACK:
                fb[0].canvas.blit(bitmap.fb[0],      v.x, v.y, 1)
                fb[1].canvas.blit(bitmap.inverted(), v.x, v.y, 0)
            elif color == YELLOW:
                fb[1].canvas.blit(bitmap.fb[0], v.x, v.y, 1)
            else:
                fb[0].canvas.blit(bitmap.inverted(), v.x, v.y, 0)
                fb[1].canvas.blit(bitmap.inverted(), v.x, v.y, 0)

