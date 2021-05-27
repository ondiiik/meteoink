from config      import sys, display_set, display_get, DISPLAY_REQUIRES_FULL_REFRESH, DISPLAY_JUST_REPAINT, DISPLAY_DONT_REFRESH
from display     import Vect, Bitmap, BLACK, WHITE, GRAY
from micropython import const


class UiFrame:
    def __init__(self, ofs, dim):
        self.ofs = ofs
        self.dim = dim
    
    
    def repaint(self, ui, d = None):
        ui.canvas.ofs += self.ofs
        r              = self.draw(ui, d)
        ui.canvas.ofs -= self.ofs
        return r


class Ui:
    def __init__(self, canvas):
        self.canvas = canvas
        self.fonts  = { 16 : {}, 25 : {}, 50 : {} , 80 : {}, 120 : {}, 160 : {} } 
    
    
    def bitmap(self, size, name):
        return Bitmap('bitmap/{}/{}.bim'.format(size, name))
    
    
    def text_center(self, size, text, pos):
        l      = self.textLength(size, text)
        pos.x -= l // 2
        return self.text(size, text, pos)
    
    
    def text_right(self, size, text, pos):
        l      = self.textLength(size, text)
        pos.x -= l
        return self.text(size, text, pos)
    
    
    def text(self, size, text, pos):
        for char in text:
            if ' ' == char:
                pos.x += int(0.3 * size) + 1
            else:
                try:
                    f                      = self.fonts[size][char]
                except KeyError:
                    f                      = Bitmap('bitmap/f/{}/{}.bim'.format(size, ord(char)))
                    self.fonts[size][char] = f
                
                self.canvas.bitmap(pos, f)
                pos.x += f.dim.x + 1
        
        return pos
    
    
    def textLength(self, size, text):
        l = 0
        for char in text:
            if ' ' == char:
                l     += int(0.3 * size) + 1
            else:
                try:
                    f                      = self.fonts[size][char]
                except KeyError:
                    f                      = Bitmap('bitmap/f/{}/{}.bim'.format(size, ord(char)))
                    self.fonts[size][char] = f
                
                l += f.dim.x + 1
        
        return l
