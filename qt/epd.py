import pygame
import framebuf



_width  = 960
_height = 540
_factor = 1
_frame  = 6



wsize = ((_frame * 2 + _width)  * _factor,
         (_frame * 2 + _height) * _factor)

_screen = pygame.display.set_mode(wsize)

pygame.draw.rect(_screen, (127, 127, 127), [0, 0, *wsize])
pygame.display.flip()

_clock  = pygame.time.Clock()

pygame.display.set_caption('EPD {} x {}'.format(_width, _height))



def _draw_pixel(x, y, c):
    pygame.draw.rect(_screen, c + c * 256 + c * 65536, [(x + _frame) * _factor, (y + _frame) * _factor, _factor, _factor])


def on():
    print('EPD ON')


def off():
    print('EPD OFF')


def power_off():
    print('EPD POWER OFF')


def clear_area(x, y, w, h):
    print('EPD Clear area {}x{}:{}+{}'.format(x, y, w, h))


def draw_image(x, y, w, h, b, t):
    print('EPD Draw area {}x{}:{}+{}'.format(x, y, w, h))
    
    fb = framebuf.FrameBuffer(b, w, h, framebuf.GS4_HMSB)
    
    for yy in range(h):
        for xx in range(w):
            _draw_pixel(xx + x, yy + y, fb.pixel(xx, yy) * 8)
    
    pygame.display.flip()
    _clock.tick(4)


BLACK_ON_WHITE = 0
