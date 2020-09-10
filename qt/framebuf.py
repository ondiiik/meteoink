MONO_HLSB = 0


_amask = (0b01111111,
          0b10111111,
          0b11011111,
          0b11101111,
          0b11110111,
          0b11111011,
          0b11111101,
          0b11111110)

_omask = (0b10000000,
          0b01000000,
          0b00100000,
          0b00010000,
          0b00001000,
          0b00000100,
          0b00000010,
          0b00000001)



class FrameBuffer:
    def __init__(self, buf, w, h, f):
        self.buf    = buf
        self.width  = w
        self.height = h
    
    
    def fill(self, c):
        for yy in range(self.height):
            for xx in range(self.width):
                self.pixel(xx, yy, c)
    
    
    def pixel(self, x, y, c = -1):
        if (x < 0) or (x > self.width) or (y < 0) or (y > self.height):
            return
        pix_index  = self.width * y + x
        byte_index = pix_index // 8
        bit_index  = pix_index %  8
        try:
            b = self.buf[byte_index]
        except:
            return c
        
        if c < 0:
            c = 0 if (b & _omask[bit_index]) == 0 else 1
        else:
            if c == 0:
                b |= _omask[bit_index]
            else:
                b &= _amask[bit_index]
            
            self.buf[byte_index] = b
            
        return c
    
    
    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            self.pixel(x,     yy, c)
            self.pixel(x + w, yy, c)
        for xx in range(x, x + w):
            self.pixel(xx, y,     c)
            self.pixel(xx, y + h, c)
    
    
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
        pass
        for yy in range(fb.height):
            for xx in range(fb.width):
                c = fb.pixel(xx, yy)
                
                if c == transparent:
                    continue
                
                self.pixel(x + xx, y + yy, c)
