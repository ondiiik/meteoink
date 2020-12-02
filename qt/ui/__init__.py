import                  heap
import                  machine
from config      import sys, display_set, display_get, DISPLAY_REQUIRES_FULL_REFRESH, DISPLAY_JUST_REPAINT, DISPLAY_DONT_REFRESH
from display     import Vect, Bitmap, BLACK, WHITE, YELLOW
from forecast    import TEMPERATURE, WEATHER, ALL
from micropython import const


heap.refresh()


class UiFrame:
    __slots__ = ('ofs', 'dim')
    
    def __init__(self, ofs, dim):
        self.ofs = ofs
        self.dim = dim
    
    
    def repaint(self, ui, d = None):
        ui.canvas.ofs += self.ofs
        r = self.draw(ui, d)
        ui.canvas.ofs -= self.ofs
        return r


class Ui:
    __slots__ = ('canvas', 'numbers')
    
    def __init__(self, canvas):
        self.canvas  = canvas
        self.numbers = { 10 : [None] * 12,
                         16 : [None] * 12,
                         25 : [None] * 12,
                         50 : [None] * 12 } 
    
    
    def bitmap(self, size, name):
        return Bitmap('bitmap/{}/{}.bim'.format(size, name))
    
    
    def text_center(self, size, text, pos, color = BLACK, corona = None, border = 2):
        l      = self.textLength(size, text)
        pos.x -= l // 2
        return self.text(size, text, pos, color, corona, border)
    
    
    def text_right(self, size, text, pos, color = BLACK, corona = None, border = 2):
        l      = self.textLength(size, text)
        pos.x -= l
        return self.text(size, text, pos, color, corona, border)
    
    
    def text(self, size, text, pos, color = BLACK, corona = None, border = 2):
        if not corona is None:
            for d in (Vect(1, 0)  * border,
                      Vect(0, 1)  * border,
                      Vect(1, 1)  * border,
                      Vect(1, -1) * border):
                self.text(size, text, pos + d, corona)
                self.text(size, text, pos - d, corona)
                
        for char in text:
            if ' ' == char:
                pos.x += int(0.3 * size) + 1
            else:
                if char in './0123456789':
                    f = self.numbers[size]
                    n = ord(char) - 0x2E
                    if f[n] == None:
                        f[n] = Bitmap('bitmap/f/{}/{}.bim'.format(size, ord(char)))
                    bitmap = f[n]
                else:
                    bitmap = Bitmap('bitmap/f/{}/{}.bim'.format(size, ord(char)))
                
                self.canvas.bitmap(pos, bitmap, color)
                pos.x += bitmap.dim.x + 1
        
        return pos
    
    
    def textLength(self, size, text):
        l = 0
        for char in text:
            if ' ' == char:
                l     += int(0.3 * size) + 1
            else:
                if char in './0123456789':
                    f = self.numbers[size]
                    n = ord(char) - 0x2E
                    if f[n] == None:
                        f[n] = Bitmap('bitmap/f/{}/{}.bim'.format(size, ord(char)))
                    l += f[n].dim.x + 1
                else:
                    l += Bitmap('bitmap/f/{}/{}.bim'.format(size, ord(char)), True).dim.x + 1
        
        return l
