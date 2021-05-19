import                    framebuf
from   config      import pins
from   micropython import const
from   struct      import unpack
import micropython


WHITE = const(15)
BLACK = const(0)
GRAY  = const(13)


class Vect:
    @micropython.native
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    @micropython.native
    def __call__(self):
        return self.x, self.y
    
    @property
    @micropython.viper
    def square(self) -> int:
        return int(self.x) * int(self.y)
    
    @micropython.viper
    def __add__(self, v):
        return Vect(int(self.x) + int(v.x),
                    int(self.y) + int(v.y))
    
    @micropython.viper
    def __sub__(self, v):
        return Vect(int(self.x) - int(v.x),
                    int(self.y) - int(v.y))
    
    @micropython.viper
    def __mul__(self, v : int):
        return Vect(int(self.x) * v,
                    int(self.y) * v)
    
    @micropython.viper
    def __div__(self, v : int):
        return Vect(int(self.x) // v,
                    int(self.y) // v)



class Bitmap:
    @micropython.native
    def __init__(self, file_name, no_load = False):
        with open(file_name, 'rb') as f:
            hdr      = unpack('<HH', f.read(4))
            self.dim = Vect(*hdr)
            
            if no_load:
                return
            
            self.buf_width = ((self.dim.x + 1) // 2) * 2
            cnt            = (self.buf_width * self.dim.y + 1) // 2
            self.buf       = bytearray(f.read(cnt))
        
        self.fb = framebuf.FrameBuffer(self.buf, self.buf_width, self.dim.y, framebuf.GS4_HMSB)
    
    @micropython.native
    def inverted(self, idx = 0):
        l   = len(self.buf[idx])
        buf = bytearray(b'\x00' * l)
        
        for i in range(l):
            buf[i] = (~self.buf[idx][i]) & 0xFF
        
        return framebuf.FrameBuffer(buf, self.buf_width, self.dim.y, framebuf.GS4_HMSB)


class Fb:
    @micropython.native
    def __init__(self, color, epd, dim):
        print("\tFB%d - [ OK ]" % color)
        
        self.epd    = epd
        self.buf    = bytearray((dim.x * dim.y + 1) // 2)
        self.canvas = framebuf.FrameBuffer(self.buf, dim.x, dim.y, framebuf.GS4_HMSB)
    
    
    @micropython.viper
    def fill(self,
             c : int):
        self.canvas.fill(c)
    
    
    @micropython.viper
    def htline(self,
               x : int,
               y : int,
               w : int,
               c : int):
        self.canvas.hline(x, y, w, 12)
    
    
    @micropython.viper
    def hline(self,
              x : int,
              y : int,
              w : int,
              c : int):
        self.canvas.hline(x, y, w, c)
    
    
    @micropython.viper
    def vtline(self,
               x : int,
               y : int,
               h : int,
               c : int):
        self.canvas.vline(x, y, h, 12)
    
    
    @micropython.viper
    def vline(self,
              x : int,
              y : int,
              h : int,
              c : int):
        self.canvas.vline(x, y, h, c)
    
    
    @micropython.viper
    def line(self,
             x1 : int,
             y1 : int,
             x2 : int,
             y2 : int,
             c  : int):
        self.canvas.line(x1, y1, x2, y2, c)
    
    
    @micropython.viper
    def rect(self,
             x : int,
             y : int,
             w : int,
             h : int,
             c : int):
        self.canvas.rect(x, y, w, h, c)
    
    
    @micropython.viper
    def fill_rect(self,
                  x : int,
                  y : int,
                  w : int,
                  h : int,
                  c : int):
        self.canvas.fill_rect(x, y, w, h, c)
    
    
    @micropython.viper
    def text(self,
             s : int,
             x : int,
             y : int,
             c : int):
        self.canvas.text(s, x, y, c)



class Canvas:
    @micropython.native
    def __init__(self):
        print("Building EPD:")
        # Load modules and set constants
        import epd
        
        # Create EPD epaper driver
        self.dim = Vect(960, 540)
        self.ofs = Vect(0, 0)
        self.epd = epd
        print("\tEPD - [ OK ]")
        
        self.fb = Fb(BLACK, epd, self.dim)
    
    
    @micropython.native
    def clear(self):
        self.fill(WHITE)
    
    
    @micropython.native
    def fill(self, c):
        self.fb.fill(c)
    
    
    @micropython.native
    def flush(self, sector = None):
        if sector is None:
            sector = 0, 0, self.dim.x, self.dim.y
        
        epd = self.epd
        epd.on()
        epd.clear_area(*sector)
        epd.draw_image(sector[0], sector[1], sector[2], sector[3], self.fb.buf, epd.BLACK_ON_WHITE)
        epd.draw_image(sector[0], sector[1], sector[2], sector[3], self.fb.buf, epd.BLACK_ON_WHITE)
        epd.power_off()
    
    
    @micropython.native
    def hline(self, v, w, c = BLACK):
        v += self.ofs
        self.fb.hline(v.x, v.y, w, c)
    
    
    @micropython.native
    def htline(self, v, w, c = BLACK):
        v += self.ofs
        self.fb.htline(v.x, v.y, w, c)
    
    
    @micropython.native
    def vtline(self, v, h, c = BLACK):
        v += self.ofs
        self.fb.vtline(v.x, v.y, h, c)
    
    
    @micropython.native
    def vline(self, v, h, c = BLACK):
        v += self.ofs
        self.fb.vline(v.x, v.y, h, c)
    
    
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
        
        self.fb.line(v1.x, v1.y, v2.x, v2.y, c)
    
    
    @micropython.native
    def rect(self, v, d, c = BLACK):
        v += self.ofs
        self.fb.rect(v.x, v.y, d.x, d.y, c)
    
    
    @micropython.native
    def fill_rect(self, v, d, c = BLACK):
        v += self.ofs
        self.fb.fill_rect(v.x, v.y, d.x, d.y, c)
    
    
    @micropython.native
    def text(self, s, v, c = BLACK):
        v += self.ofs
        self.fb.text(s, v.x, v.y, c)
    
    
    @micropython.native
    def bitmap(self, v, bitmap):
        v  += self.ofs
        fb  = self.fb
        fb.canvas.blit(bitmap.fb, v.x, v.y, 1)

