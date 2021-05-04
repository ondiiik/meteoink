from machine  import deepsleep, reset
from esp32    import raw_temperature
from config   import sys, vbat, display_set, display_get, DISPLAY_REQUIRES_FULL_REFRESH, DISPLAY_GREETINGS
from buzzer   import play
from vbat     import voltage
from led      import Led
from display  import Canvas
from net      import Connection
import               jumpers
from forecast import Forecast
from ui.main  import MeteoUi
from web.main import WebServer


def run(sha):
    # Checks if we are running right micropython firmware
    # This firmware expects some parts as built in, so the
    # exact firmware built ID to be present. Modules, which
    # is used for detection is pyptf (python platform).
    try:
        from pyptf import KERNEL_VARIANT
        
        if not 3 == KERNEL_VARIANT:
            raise RuntimeError()
    except:
        raise RuntimeError('''Incompatible micropython firmware found!
Please download right one here:
\t\thttps://github.com/ondiiik/meteoink/blob/master/esp32
''')
    
    
    # Reads internal temperature just after wake-up to reduce
    # influence of chip warm-up and use some kind of ambient
    # reduction to get more close to indoor temperature. This
    # value will be used when DTH22 or DHT11 sensor is
    # not found on selected pin.
    # 
    # Just note that better is to connect DHT22/DTH11 for
    # more precise temperature measurement and also for information
    # about humidity.
    temp = ((raw_temperature() - 32) / 1.8) - 34.0
    
    # There is LED driver for debugging purposes. LED control
    # is running on background and can be disabled to save
    # piece of battery capacity. However then there is no
    # other way how to signalizes in which state meteostation
    # is then UART.
    led = Led()
    
    # Disable LED when battery voltage is too low
    volt = voltage()
    
    if (volt < vbat.VBAT_LOW):
        led.disable()
    
    # As we uses E-Ink display, the most comfortable way
    # how to work with it is to define canvas object for
    # drawing objects and flushing them later on screen.
    led.mode(Led.WARM_UP)
    canvas = Canvas()
    
    # When battery voltage is too low, just draw low battery
    # error on screen and go to deep sleep.
    if (volt < vbat.VBAT_LOW):
        led.mode(Led.ALERT)
        
        ui = MeteoUi(canvas, None, None)
        ui.repaint_lowbat(volt)
        
        print('Going to deep sleep ...')
        deepsleep(120000)
    
    # Once we have canvas established (large object needs
    # to be created first to prevent from memory fragmentation),
    # we can establish WiFi connection and connect to network.
    led.mode(Led.DOWNLOAD)
    
    try:
        net = Connection()
    except:
        net = None
    
    # It can happen that we want only to move meteostation somewhere
    # and don't want to let it wake up during transport. In this case
    # we can put it to greetings mode, where only picture is displayed
    # and station kept sleeping till reset button is pressed
    if DISPLAY_GREETINGS == display_get():
        ui = MeteoUi(canvas, None, net)
        ui.repaint_welcome(led)
        
        print('Going to deep sleep ...')
        display_set(DISPLAY_REQUIRES_FULL_REFRESH)
        deepsleep()
    
    # It may happen that user wants to attach with HTTP for update of firmware
    # or configuration. In this case we can not rely on existing WiFi connection
    # and we rather go to hot-spot mode.
    elif jumpers.hotspot:
        play(((2093, 30), (0, 120),(2093, 30)))
        led.mode(Led.DOWNLOAD)
        
        ui = MeteoUi(canvas, None, net)
        ui.repaint_config(led, volt)
        led.mode(Led.DOWNLOAD)
        del ui, canvas, led, volt
        
        server = WebServer(net)
        
        play(((1047, 30), (0, 120), (1319, 30), (0, 120), (1568, 30), (0, 120), (2093, 30)))
        server.run()
        
        reset()
    
    # And finally - meteostation display - basic functionality ;-)
    else:
        # Network is running and connected ... we can checks for updates
        if sys.AUTOUPDATE and not net is None:
            from autoupdate import do_update
            do_update(sha)
        
        # Once we are connected on network, we can download forecast.
        # Just note that once forecast is download, WiFi is disconnected
        # to save as much battery capacity as possible.
        if not net is None:
            forecast = Forecast(net, temp)
        else:
            forecast = None
        
        # Most time consuming part when we have all data is to draw them
        # on user interface - screen.
        ui = MeteoUi(canvas, forecast, net)
        ui.repaint_weather(led, volt)
        
        del ui, canvas
        if not net is None:
            net = True
        
        # Forecast is painted. Now we shall checks how about temperature
        # or low battery notification and produce alert sound if needed.
        if False:
            for i in range(3):
                play(((1000,30), (0,30),(1000,30), (0,30),(1000,30), (0,100)))
        
        # When all is displayed, then go to deep sleep. Sleep time is obtained
        # according to current weather forecast and UI needs ans is in minutes.
        print('Going to deep sleep ...')
        if net is None:
            deepsleep(60000)
        else:
            deepsleep(forecast.status.sleep_time * 60000)
