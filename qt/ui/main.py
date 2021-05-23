from   .           import Ui
from   config      import display_set, display_get, hotspot, DISPLAY_REQUIRES_FULL_REFRESH, DISPLAY_JUST_REPAINT, DISPLAY_DONT_REFRESH
from   display     import Vect, WHITE
from   forecast    import TEMPERATURE, WEATHER, ALL
from   micropython import const
import machine


_CHART_HEIGHT    = const(70)
_CHART_ICON_SIZE = const(90)
_CHART_POS       = const(530 - _CHART_HEIGHT - _CHART_ICON_SIZE)
_CHART_TAIL      = const(480 - _CHART_HEIGHT)
_CHART_RAIN      = const(35  + _CHART_TAIL)
_CHART_HEAD      = const(385 - _CHART_HEIGHT - _CHART_ICON_SIZE)
_CHART_ICON_POS  = const(80  + _CHART_HEAD)
_DATA_SIZE       = const(590 - _CHART_POS)
_DATA_LOWER      = const(140)

class Epd47(Ui):
    def __init__(self, canvas, forecast, connection):
        super().__init__(canvas)
        self.forecast   = forecast
        self.connection = connection
    
    
    def repaint_welcome(self, led):
        # Redraw display
        print('Drawing welcome ...')
        led.mode(led.DRAWING)
        
        bitmap = self.bitmap(1, 'greetings')
        self.canvas.bitmap(Vect(0, 0), bitmap)
        
        print('Flushing ...')
        led.mode(led.FLUSHING)
        self.canvas.flush()
    
    
    def repaint_weather(self, led, volt):
        # Redraw display
        print('Drawing weather ...')
        led.mode(led.DRAWING)
        
        self.canvas.fill(WHITE)
        
        # We have forecast, so lets draw it on screen. Don't draw
        # always everything as forecast is changing not so often,
        # but temperature is.
        status = self.forecast.status
        
        if not status.refresh == TEMPERATURE:
            weather_dr(self, Vect(0, 0),             Vect(960, 100))
            outside_dr(self, Vect(145, _DATA_LOWER), Vect(295, 50))
            
        winfo_dr(  self, Vect(105, -5), Vect(385, 50))
        outtemp_dr(self, Vect(105, 60), Vect(295, 50))
        #
        if status.refresh == ALL:
            cal_dr(self, Vect(0, _CHART_HEAD), Vect(960, 26))
            
        if not status.refresh == TEMPERATURE:
            inside_dr(self, Vect(640, _DATA_LOWER), Vect(295, _DATA_SIZE // 2))
            vbat_dr(  self, Vect(432, 16),          Vect(48, 30), volt)
        
        intemp_dr(self, Vect(640, 0), Vect(295, _DATA_SIZE))
        
        if status.refresh == ALL:
            cal_dr(  self, Vect(0, _CHART_TAIL),     Vect(960, _CHART_HEIGHT), False)
            tempg_dr(self, Vect(0, _CHART_RAIN),     Vect(960, _CHART_HEIGHT))
            icons_dr(self, Vect(0, _CHART_ICON_POS), Vect(960, _CHART_ICON_SIZE))
            rain_dr( self, Vect(0, _CHART_RAIN),     Vect(960, _CHART_HEIGHT))
            tempt_dr(self, Vect(0, _CHART_RAIN),     Vect(960, _CHART_HEIGHT))
        
        # Flush drawing on display (upper or all parts)
        print('Flushing ...')
        led.mode(led.FLUSHING)
        
        if   status.refresh == TEMPERATURE:
            self.canvas.flush((124, 0, 92, 98))
        elif status.refresh == WEATHER:
            self.canvas.flush((0, 0, 400, 98))
        else:
            self.canvas.flush()
        
        # Display is repainted, so next can be just partial repaint
        display_set(DISPLAY_JUST_REPAINT)
    
    
    def repaint_config(self, led, volt):
        from config.spot import hotspot
        
        # After config we will need to repaint all
        display_set(DISPLAY_REQUIRES_FULL_REFRESH)
        
        print('Drawing config ...')
        led.mode(led.DRAWING)
        self.canvas.fill(WHITE)
        
        qr_dr(self,
              Vect(0, 0),
              Vect(0, 0),
              ('WIFI:T:WPA;S:{};P:{};;'.format(hotspot.ssid, hotspot.passwd), 'WiFi', False));
        
        url = 'http://{}:5555'.format('192.168.4.1')
        qr_dr(self, Vect(716, 320), Vect(0, 0), (url, 'Config URL', True));
        
        url_dr(self,  Vect(0,   self.canvas.dim.y // 2), Vect(self.canvas.dim.x - 132, self.canvas.dim.y // 2), url)
        wifi_dr(self, Vect(250, 0),                      Vect(self.canvas.dim.x - 132, self.canvas.dim.y // 2), hotspot)
        
        vbat_dr(self,  Vect(self.canvas.dim.x // 2 - 10, self.canvas.dim.y // 2),  Vect(48, 30), volt)
        
        print('Flushing ...')
        led.mode(led.FLUSHING)
        self.canvas.flush()
        
        with open('mode.py', 'w') as f:
            f.write('MODE = 1')
        
        machine.reset()
    
    
    def repaint_lowbat(self, volt):
        if not display_get() == DISPLAY_DONT_REFRESH:
            print('Drawing lowbat ...')
            self.canvas.fill(WHITE)
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
    UiOutTemp(p, d).repaint(ui)

def inside_dr(ui, p, d):
    from ui.inside import UiInside
    UiInside(p, d).repaint(ui)

def winfo_dr(ui, p, d):
    from ui.winfo import UiWInfo
    UiWInfo(p, d).repaint(ui)

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




class MeteoUi:
    def __init__(self, canvas, forecast, connection):
        self.ui              = Epd47(canvas, forecast, connection)
        self.repaint_welcome = self.ui.repaint_welcome
        self.repaint_weather = self.ui.repaint_weather
        self.repaint_config  = self.ui.repaint_config
        self.repaint_lowbat  = self.ui.repaint_lowbat

