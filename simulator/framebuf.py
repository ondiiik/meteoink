GS4_HMSB = 0


class FrameBuffer:
    def __init__(self, buf, w, h, f):
        self._buf = buf
        self._width = w
        self._height = h

    def fill(self, c):
        p = (c << 4) | c
        for i in range(len(self._buf)):
            self._buf[i] = p

    def pixel(self, x, y, c=-1):
        if x not in range(self._width) or y not in range(self._height):
            return c

        pix_index = self._width * y + x
        byte_index = pix_index // 2
        bit_index = 4 - (pix_index % 2) * 4

        try:
            b = self._buf[byte_index]
        except:
            return c

        if c < 0:
            c = (b >> bit_index) & 0xF
        else:
            m = 0xF0 >> bit_index
            b = c << bit_index
            self._buf[byte_index] &= m
            self._buf[byte_index] |= b

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
            FrameBuffer.hline(self, x, yy, w, c)

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
                x1, x2 = x2, x1
                y1, y2 = y2, y1

            for x in range(x1, x2):
                y = y1 + dy * (x - x1) / dx
                self.pixel(int(x), int(y), c)
        else:
            if y1 > y2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1

            for y in range(y1, y2):
                x = x1 + dx * (y - y1) / dy
                self.pixel(int(x), int(y), c)

    def blit(self, fb, x, y, transparent=-1):
        for yy in range(fb._height):
            for xx in range(fb._width):
                c = fb.pixel(xx, yy)

                if c == transparent:
                    continue

                self.pixel(x + xx, y + yy, c)
