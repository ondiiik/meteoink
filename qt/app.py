def run():
    try:
#     if True:
        # Reads internal temerature just after wake-up to reduce
        # influence of chip warm-up and use some kind of ambient
        # reduction to get more close to indoor temperature. This
        # value will be used when DTH22 sensor is not found on
        # pin 23.
        # 
        # Just note that better is to connect DHT22 to pin 23 for
        # more precise temperature and also for information about
        # humidity.
        from esp32 import raw_temperature
        temp = ((raw_temperature() - 32) / 1.8) - 34.0
        
        # As we use bi-color E-Ink display, it consumes big amount
        # of memory for frame buffers. Therefore we have to call
        # tweak and call garbage collector aggressively.
        import heap
        heap.refresh()
        
        # There is LED driver for debugging purposes. LED control
        # is running in separate thread and can be disabled to save
        # piece of battery capacity. However then there is no way
        # how to signalizes in which state meteostation is.
        from led import Led
        led = Led()
        heap.refresh()
        
        # As we uses E-Ink display, the most comfortable way
        # how to work with it is to define canvas object for
        # drawing objects and flushing them later to screen.
        led.mode(Led.ON)
        from display import Canvas
        canvas = Canvas()
        heap.refresh()
        
        # Once we have canvas established (large object needs
        # to be created first to prevent from memory fragmentation),
        # we can establish WiFi connection and connect to network.
        led.mode(Led.FLASH1)
        from net import Connection
        net = Connection()
        heap.refresh()
        
        # Following parts are relevant in normal mode (draw forecast)
        from jumpers import meteostation, alert
        from buzzer  import play
        
        if meteostation():
            # Once we are connected on network, we can download forecast.
            # Just note that once forecast is download, WiFi is disconnected
            # to save as much battery capacity as possible.
            from forecast import Forecast
            forecast = Forecast(net, temp)
            heap.refresh()
            
            # We extract time of current weather from obtained data. Special
            # object for this purposes is used because obtained time is in
            # unix 'since epoch' format (related to year 1970) but ESP32 uses
            # epoch year 2000. We also shall correct according to time zone. 
            from ltime import Time
            time = Time(forecast.time_zone)
            
            # Most time consuming part when we have all data is to draw them
            # on user interface - screen.
            led.mode(Led.FLASH2)
            from ui import Ui
            ui = Ui(canvas, forecast, net)
            heap.refresh()
            ui.repaint_weather()
            heap.refresh()
            
            # Forecast is painted. Now we shall checks how about temperature
            # or low battery notification and produce alert sound if needed.
            if alert():
                for i in range(3):
                    play(((1000,30), (0,30),(1000,30), (0,30),(1000,30), (0,100)))
            
            # When all is displayed, then go to deep sleep. Sleep time is obtained
            # according to current weather forecast and UI needs ans is in minutes.
            import machine
            led.running = False
            machine.deepsleep(forecast.status.refresh * 60000)
            
        # It may happen that user wants to attach with HTTP for
        # update of firmware or configuration
        else:
            play(((2093, 30), (0, 120),(2093, 30)))
            led.mode(Led.FLASH2)
            
            from web     import Server
            from machine import reset
            from ui      import Ui
            
            ui = Ui(canvas, None, net)
            ui.repaint_config()
            heap.refresh()
            
            led.mode(Led.ON)
            server = Server(net)
            
            play(((1047, 30), (0, 120), (1319, 30), (0, 120), (1568, 30), (0, 120), (2093, 30)))
            server.run()
            
            reset()
    
    except:
        import heap
        heap.refresh()
         
        from machine import reset
        from buzzer  import play
         
        led.mode(Led.ALERT)
         
        for i in range(6):
            play(((784, 500), (523, 500)))
         
        reset()
