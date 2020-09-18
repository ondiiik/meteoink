def run(sha):
    import machine
    from   config import sys, reset_counter_get, reset_counter_set
    from   buzzer import play
    
#     try:
    if True:
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
        
        # Slow nown a bit and save piece of battery
        machine.freq(sys.FREQ_MIN)
        
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
        
        # Disable LED when brown-out (too low battery reset)
        # is detected
        if (machine.reset_cause() == machine.PWRON_RESET) and (reset_counter_get() > 0):
            led.disable()
        
        # As we uses E-Ink display, the most comfortable way
        # how to work with it is to define canvas object for
        # drawing objects and flushing them later to screen.
        led.mode(Led.WARM_UP)
        from display import Canvas
        canvas = Canvas()
        heap.refresh()
        
        # Checks reset cause for potential brown-out
        # (too low battery) reset. This is considered when two
        # consecutive resets are detected.
        if machine.reset_cause() == machine.PWRON_RESET:
            if reset_counter_get() > 0:
                from ui import Ui
                led.mode(Led.ALERT)
                
                ui = Ui(canvas, None, None)
                heap.refresh()
                ui.repaint_lowbat()
                heap.refresh()
                
                print('Going to deep sleep ...')
                machine.deepsleep(120000)
            else:
                reset_counter_set(1)
        
        # We have to set high CPU speed due to compatibility with WiFi HW
        machine.freq(sys.FREQ_MAX)
        
        # Once we have canvas established (large object needs
        # to be created first to prevent from memory fragmentation),
        # we can establish WiFi connection and connect to network.
        led.mode(Led.DOWNLOAD)
        from net import Connection
        net = Connection()
        heap.refresh()
        
        
        # Network is running ... we can checks for updates
        if sys.AUTOUPDATE:
            from autoupdate import do_update
            do_update(sha)
        
        # Following parts are relevant in normal mode (draw forecast)
        from jumpers import meteostation, alert
        
        if meteostation():
            # Once we are connected on network, we can download forecast.
            # Just note that once forecast is download, WiFi is disconnected
            # to save as much battery capacity as possible.
            from forecast import Forecast
            forecast = Forecast(net, temp)
            heap.refresh()
            
            # Most time consuming part when we have all data is to draw them
            # on user interface - screen.
            from ui import Ui
            ui = Ui(canvas, forecast, net)
            heap.refresh()
            ui.repaint_weather(led)
            heap.refresh()
            
            # Forecast is painted. Now we shall checks how about temperature
            # or low battery notification and produce alert sound if needed.
            if alert():
                for i in range(3):
                    play(((1000,30), (0,30),(1000,30), (0,30),(1000,30), (0,100)))
            
            # All runs fine - annulate counter reset
            reset_counter_set(0)
            
            # When all is displayed, then go to deep sleep. Sleep time is obtained
            # according to current weather forecast and UI needs ans is in minutes.
            print('Going to deep sleep ...')
            machine.deepsleep(forecast.status.sleep_time * 60000)
            
        # It may happen that user wants to attach with HTTP for
        # update of firmware or configuration
        else:
            play(((2093, 30), (0, 120),(2093, 30)))
            led.mode(Led.DOWNLOAD)
            
            from web import Server
            from ui  import Ui
            
            ui = Ui(canvas, None, net)
            ui.repaint_config(led)
            heap.refresh()
            
            led.mode(Led.DOWNLOAD)
            server = Server(net)
            
            play(((1047, 30), (0, 120), (1319, 30), (0, 120), (1568, 30), (0, 120), (2093, 30)))
            server.run()
            
            machine.reset()
    
#     except:
#         import heap
#         heap.refresh()
#          
#         led.mode(Led.ALERT)
#          
#         for i in range(6):
#             play(((784, 500), (523, 500)))
#          
#         machine.reset()
