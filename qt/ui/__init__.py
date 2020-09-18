import                    heap
import                    machine
from   config      import sys, display_set, display_get, DISPLAY_REQUIRES_FULL_REFRESH, DISPLAY_JUST_REPAINT, DISPLAY_DONT_REFRESH
from   display     import Color, Vect, Bitmap 
from   micropython import const


heap.refresh()


_CHART_HEIGHT = const(100)


class UiFrame:
    def __init__(self, ofs, dim):
        self.ofs = ofs
        self.dim = dim
    
    
    def repaint(self, ui, d = None):
        ui.canvas.ofs += self.ofs
        r = self.draw(ui, d)
        ui.canvas.ofs -= self.ofs
        return r
    
    
    
    
class Ui:
    def __init__(self, canvas, forecast, connection):
        __slots__ = ('canvas', 'forecast', 'time', 'connection')
        self.canvas     = canvas
        self.forecast   = forecast
        self.connection = connection
    
    
    def bitmap(self, size, name):
        return Bitmap('bitmap/{}/{}.bim'.format(size, name))
    
    
    def text_center(self, size, text, pos, color = Color.BLACK, corona = None, border = 2):
        l      = self.textLength(size, text)
        pos.x -= l // 2
        return self.text(size, text, pos, color, corona, border)
    
    
    def text_right(self, size, text, pos, color = Color.BLACK, corona = None, border = 2):
        l      = self.textLength(size, text)
        pos.x -= l
        return self.text(size, text, pos, color, corona, border)
    
    
    def text(self, size, text, pos, color = Color.BLACK, corona = None, border = 2):
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
                bitmap = Bitmap('bitmap/f/{}/{}.bim'.format(size, ord(char)), True)
                l     += bitmap.dim.x + 1
        
        return l
    
    
    def repaint_weather(self, led, volt):
        # For drawing burst CPU to full power
        machine.freq(sys.FREQ_MAX)
        
        # Redraw display
        print('Drawing ...')
        led.mode(led.DRAWING)
        
        self.canvas.fill(Color.WHITE)
        heap.refresh()
        
        status = self.forecast.status
        
        if not status.refresh == self.forecast.TEMPERATURE:
            weather_dr(self, Vect(0,   0), Vect(400, 100))
            heap.refresh()
            l = outside_dr(self, Vect(105, 0), Vect(295, 50))
            heap.refresh()
        
        outtemp_dr(self, Vect(105, 0), Vect(295, 50))
        heap.refresh()
        
        if status.refresh == self.forecast.ALL:
            cal_dr(self, Vect(0, 100), Vect(400, 20))
            heap.refresh()
        
        if not status.refresh == self.forecast.TEMPERATURE:
            inside_dr(self, Vect(105, 50), Vect(295, 50), l, self.connection)
            heap.refresh()
            vbat_dr(  self, Vect(284, 87), Vect(14, 10), volt)
            heap.refresh()
            
        intemp_dr(self, Vect(105, 50), Vect(295, 50))
        heap.refresh()
        
        heap.refresh()
        if status.refresh == self.forecast.ALL:
            cal_dr(  self, Vect(0, 170), Vect(400, _CHART_HEIGHT + 5), False)
            heap.refresh()
            tempg_dr(self, Vect(0, 170), Vect(400, _CHART_HEIGHT))
            heap.refresh()
            icons_dr(self, Vect(0, 128), Vect(400, 40))
            heap.refresh()
            wind_dr( self, Vect(0, 282), Vect(400, 20))
            heap.refresh()
            rain_dr( self, Vect(0, 170), Vect(400, _CHART_HEIGHT))
            heap.refresh()
            tempt_dr(self, Vect(0, 170), Vect(400, _CHART_HEIGHT))
            heap.refresh()
        
        # For flushing we can slow down as this uses busy wait and
        # SPI communication
        machine.freq(sys.FREQ_MIN)
        
        # Flush drawing on display (upper or all parts)
        print('Flushing ...')
        led.mode(led.FLUSHING)
        
        if status.refresh == self.forecast.TEMPERATURE:
            self.canvas.flush((124, 0, 92, 98))
        elif status.refresh == self.forecast.WEATHER:
            self.canvas.flush((0, 0, 400, 98))
        else:
            self.canvas.flush()
        
        # Display is repainted, so next can be just partial repaint
        display_set(DISPLAY_JUST_REPAINT)
    
    
    def repaint_config(self, led, volt):
        from config.spot import hotspot
        
        # After config we will need to repaint all
        display_set(DISPLAY_REQUIRES_FULL_REFRESH)
        
        print('Drawing ...')
        led.mode(led.DRAWING)
        self.canvas.fill(Color.WHITE)
        
        qr_dr(self,
              Vect(0, 0),
              Vect(0, 0),
              ('WIFI:T:WPA;S:{};P:{};;'.format(hotspot.ssid, hotspot.passwd), 'WiFi', False));
        heap.refresh()
        
        url = 'http://{}:5555'.format(self.connection.ifconfig[0])
        qr_dr(self, Vect(278, 178), Vect(0, 0), (url, 'Config URL', True));
        heap.refresh()
        
        url_dr(self,  Vect(0,   self.canvas.dim.y // 2), Vect(self.canvas.dim.x - 132, self.canvas.dim.y // 2), url)
        wifi_dr(self, Vect(200, 0),                      Vect(self.canvas.dim.x - 132, self.canvas.dim.y // 2), hotspot)
        
        vbat_dr(self,  Vect(self.canvas.dim.x // 2 - 10, self.canvas.dim.y // 2),  Vect(20, 10), volt)
        
        print('Flushing ...')
        led.mode(led.FLUSHING)
        self.canvas.flush()
    
    
    def repaint_lowbat(self, volt):
        if not display_get() == DISPLAY_DONT_REFRESH:
            print('Drawing ...')
            self.canvas.fill(Color.WHITE)
            v = Vect(self.canvas.dim.x // 2 - 30, self.canvas.dim.y // 2)
            d = Vect(60, 30)
            vbat_dr(self, v, d, volt)
            
            print('Flushing ...')
            self.canvas.flush((v.x - 20, v.y - 26, d.x + 46, d.y + 40))
            
            display_set(DISPLAY_DONT_REFRESH)
        else:
            print('Already painted ... saving battery')


def weather_dr(ui, p, d):
    from ui.weather import UiWeather
    UiWeather(p, d).repaint(ui)

def outside_dr(ui, p, d):
    from ui.outside import UiOutside
    return UiOutside(p, d).repaint(ui)

def outtemp_dr(ui, p, d):
    from ui.outtemp import UiOutTemp
    return UiOutTemp(p, d).repaint(ui)

def inside_dr(ui, p, d, tab, connection):
    from ui.inside import UiInside
    UiInside(p, d).repaint(ui, (tab, connection))

def intemp_dr(ui, p, d):
    from ui.intemp import UiInTemp
    UiInTemp(p, d).repaint(ui)

def cal_dr(ui, p, d, title = True):
    from ui.calendar import UiCalendar
    UiCalendar(p, d).repaint(ui, title)

def icons_dr(ui, p, d):
    from ui.icons import UiIcons
    UiIcons(p, d).repaint(ui)

def rain_dr(ui, p, d):
    from ui.rain import UiRain
    UiRain(p, d).repaint(ui)

def tempg_dr(ui, p, d):
    from ui.tempg import UiTempGr
    UiTempGr(p, d).repaint(ui)

def wind_dr(ui, p, d):
    from ui.wind import UiWind
    UiWind(p, d).repaint(ui)

def tempt_dr(ui, p, d):
    from ui.tempt import UiTempTxt
    UiTempTxt(p, d).repaint(ui)

def fore_dr(ui, p, d):
    from ui.forecast import UiForecast
    UiForecast(p, d).repaint(ui)

def qr_dr(ui, p, d, a):
    from ui.qr import UiQr
    UiQr(p, d, a).repaint(ui)

def wifi_dr(ui, p, d, h):
    from ui.wifi import UiWifi
    UiWifi(p, d, h).repaint(ui)

def url_dr(ui, p, d, u):
    from ui.url import UiUrl
    UiUrl(p, d, u).repaint(ui)
    
def vbat_dr(ui, p, d, volt):
    from ui.vbat import UiVBat
    UiVBat(p, d).repaint(ui, volt)
