import pygame
import framebuf


LANDSCAPE     = 0
LUT_64K       = 2
FEED_QUEUE_32 = 8


class Epd:
    WIDTH  = 960
    HEIGHT = 540
    
    
    def __init__(self):
        def _iter():
            for i in range(Epd.WIDTH * Epd.HEIGHT // 2):
                yield 255
        
        self._fb = bytearray(_iter())
    
    
    def fb(self):
        return self._fb
    
    
    def on(self):
        print('EPD ON')
    
    
    def off(self):
        print('EPD OFF')
    
    
    def power_off(self):
        print('EPD POWER OFF')
    
    
    def clear_area(self, x, y, w, h):
        print('EPD Clear area {}x{}:{}+{}'.format(x, y, w, h))
    
    
    def flush(self):
        print('EPD Draw area {}x{}:{}+{}'.format(0, 0, Epd.WIDTH, Epd.HEIGHT))
        
        fb = framebuf.FrameBuffer(self._fb, Epd.WIDTH, Epd.HEIGHT, framebuf.GS4_HMSB)
        
        for yy in range(Epd.HEIGHT):
            for xx in range(Epd.WIDTH):
                _draw_pixel(xx, yy, fb.pixel(xx, yy) * 8)
        
        pygame.display.flip()
        _clock.tick(4)



_factor = 1
_frame  = 6

wsize = ((_frame * 2 + Epd.WIDTH)  * _factor,
         (_frame * 2 + Epd.HEIGHT) * _factor)

_screen = pygame.display.set_mode(wsize)

pygame.draw.rect(_screen, (127, 127, 127), [0, 0, *wsize])
pygame.display.flip()

_clock  = pygame.time.Clock()

pygame.display.set_caption('EPD {} x {}'.format(Epd.WIDTH, Epd.HEIGHT))



def _draw_pixel(x, y, c):
    pygame.draw.rect(_screen, c + c * 256 + c * 65536, [(x + _frame) * _factor, (y + _frame) * _factor, _factor, _factor])


BLACK_ON_WHITE = 0
