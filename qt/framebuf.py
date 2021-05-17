MONO_HLSB = 0
MONO_VLSB = 1
GS4_HMSB  = 2
MHLSB     = MONO_HLSB
MVLSB     = MONO_VLSB

_mask     = (0b11110000, 0b00001111)
_shift    = (0, 4)



class FrameBuffer:
    def __init__(self, buf, w, h, f):
        self.buf    = buf
        self.width  = w
        self.height = h
    
    def fill(self, c):
        p = c | c << 4
        for i in range(len(self.buf)):
            self.buf[i] = p
    
    def pixel(self, x, y, c = -1):
        if (x < 0) or (x > self.width) or (y < 0) or (y > self.height):
            return c
            
        pix_index  = self.width * y + x
        byte_index = pix_index // 2
        bit_index  = pix_index %  2
        
        try:
            b = self.buf[byte_index]
        except:
            return c
            
        if c < 0:
            c = (b >> _shift[bit_index]) & 0xF
        else:
            b &= _mask[bit_index]
            b |= (c << _shift[bit_index])
            self.buf[byte_index] = b
            
        return c
    
    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h - 1):
            self.pixel(x,     yy, c)
            self.pixel(x + w - 1, yy, c)
        for xx in range(x, x + w - 1):
            self.pixel(xx, y,     c)
            self.pixel(xx, y + h - 1, c)
    
    def fill_rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            self.hline(x, yy, w, c)
    
    def vline(self, x, y, h, c):
        for yy in range(y, y + h):
            self.pixel(x, yy, c)
    
    def hline(self, x, y, w, c):
        for xx in range(x, x + w):
            self.pixel(xx, y, c)
    
    def line(self, x1, y1, x2, y2, c):
        dx = x2 - x1
        dy = y2 - y1
        
        if abs(dx) > abs(dy):
            if x1 > x2:
                x  = x2
                x2 = x1
                x1 = x
                y  = y2
                y2 = y1
                y1 = y
                
            for x in range(x1, x2):
                y = y1 + dy * (x - x1) / dx
                self.pixel(int(x), int(y), c)
        else:
            if y1 > y2:
                x  = x2
                x2 = x1
                x1 = x
                y  = y2
                y2 = y1
                y1 = y
                
            for y in range(y1, y2):
                x = x1 + dx * (y - y1) / dy
                self.pixel(int(x), int(y), c)
    
    def blit(self, fb, x, y, transparent = -1):
        for yy in range(fb.height):
            for xx in range(fb.width):
                c = fb.pixel(xx, yy)
                
                if c == transparent:
                    continue
                    
                self.pixel(x + xx, y + yy, c)
