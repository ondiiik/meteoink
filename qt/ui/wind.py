from ui import Vect, Color, UiFrame
import         heap


def drawWind(ui, pos, weather, scale = 16, arrow = False):
    def rescale(v):
        return v * scale // 16
    
    if weather.speed < 2.5:
        ui.canvas.fill_rect(Vect(rescale(-2), rescale(-2)) + pos,
                            Vect(rescale( 4), rescale( 4)),
                            Color.BLACK)
        return
    
    from cmath import rect, pi
    r = rescale(30)
    o = pos.x + pos.y * 1j
    d = rect(r, (weather.dir - 90) * pi / 180)
    
    d2 = o - d
    
    def drawArrow(r, c, w):
        if   weather.speed < 5:
            r = r * 2 // 3
        elif weather.speed > 7:
            w += 1
            
        d1 = d2 + rect(r * 2, (weather.dir - 75) * pi / 180)
        ui.canvas.line(Vect(int(d1.real), int(d1.imag)), Vect(int(d2.real), int(d2.imag)), c, w)
        ui.canvas.line(Vect(int(d1.real), int(d1.imag)), Vect(int(o.real),  int(o.imag)),  c, w)
        
        d1 = d2 + rect(r * 2, (weather.dir - 105) * pi / 180)
        ui.canvas.line(Vect(int(d1.real), int(d1.imag)), Vect(int(d2.real), int(d2.imag)), c, w)
        ui.canvas.line(Vect(int(d1.real), int(d1.imag)), Vect(int(o.real),  int(o.imag)),  c, w)
    
    if weather.speed > 10:
        c = Color.YELLOW
    else:
        c = Color.WHITE
    
    if weather.speed > 16:
        w = 6
    else:
        w = 3
        
    drawArrow(r, c,           w)
    drawArrow(r, Color.BLACK, 1)
    
    if not arrow:
        d1 = o - 0.4 * d
        d  = o + d
        
        def drawWindSpeed(w, c):
            ui.canvas.line(Vect(int(d.real), int(d.imag)), Vect(int(d1.real), int(d1.imag)), c, w)
            
            for i in range(int(weather.speed / 2.5)):
                rr  = r  - rescale(7) * (i // 2) - rescale(5)
                l   = rescale(15 + 10 * (i %  2))
                b   = rect(rr, (weather.dir - 90) * pi / 180) + o
                e   = rect(l,  (weather.dir - 30) * pi / 180) + b
                ui.canvas.line(Vect(int(b.real), int(b.imag)), Vect(int(e.real), int(e.imag)), c, w)
                
        w = rescale(2) + 1
        drawWindSpeed(w + 1, Color.WHITE)
        drawWindSpeed(w,     Color.BLACK)


class UiWind(UiFrame):
    def __init__(self, ofs, dim):
        super().__init__(ofs, dim)
        
    def draw(self, ui, d):
        forecast = ui.forecast.forecast
        cnt      = len(forecast)
        
        for i in reversed(range(cnt)):
            heap.refresh()
            x = ui.canvas.dim.x * i // (cnt + 1) + 5
            y = (i % 2) * -7 + 10
            drawWind(ui, Vect(x, y), forecast[i], 4, True)
