from jumpers  import jumpers
from network  import WLAN, STA_IF, AP_IF
from config   import connection, hotspot
from utime    import sleep
from var.mode import MODE
from log      import log
from uerrno   import ECONNABORTED, ENOBUFS


class Wifi:
    def __init__(self, ssid, bssid):
        self.ssid  = ssid
        self.bssid = bssid


class NoWifiError(RuntimeError):
    def __init__(self):
        super().__init__("No known WiFi found!")


class JsonError(ValueError):
    def __init__(self, e):
        super().__init__(e)


class Connection:
    def __init__(self):
        # Scan networks in surrounding
        self._ifc = WLAN(STA_IF)
        
        if not self._ifc.active(True):
            raise RuntimeError("WiFi activation failed")
        
        sc        = self._ifc.scan()
        self.nets = []
        
        for n in sc:
            self.nets.append(Wifi(n[0].decode(), n[1]))
        
        self._ifc.active(False)
        
        # Start requested variant of connection
        if jumpers.hotspot or MODE == 1:
            self._hotspot()
        else:
            self._attach()
    
    
    def _attach(self):
        # Activate WiFi interface
        self._ifc = WLAN(STA_IF)
        
        if not self._ifc.active(True):
            raise RuntimeError("WiFi activation failed")
        
        # Search first based on BSSID
        network = None
        
        for n in self.nets:
            for c in connection:
                if n.bssid == c.bssid:
                    network = c
                    break
            else:
                continue
            break
        
        # Repeat the same for SSID if BSSID was not found
        if network is None:
            for n in self.nets:
                for c in connection:
                    if n.ssid == c.ssid:
                        network = c
                        break
                else:
                    continue
                break
        
        # Checks if we have something and connect to WiFi
        if network is None:
            raise NoWifiError()
        
        self.config = network
        
        self._ifc.connect(network.ssid, network.passwd, bssid = network.bssid)
        
        for i in range(8):
            if self._ifc.isconnected():
                log("Connected: " + str(self.ifconfig))
                self.is_hotspot = False
                return
            
            sleep(1)
            
        raise RuntimeError("Wifi connection refused")
    
    
    def _hotspot(self):
        # Create hotspot to be able to attach by FTP and configure meteostation
        self._ifc = WLAN(AP_IF)
        self._ifc.active(True)
        self._ifc.config(essid = hotspot.ssid, password = hotspot.passwd, authmode = 3)
        
        while self._ifc.active() == False:
            sleep(1)
        
        self.is_hotspot = True
        log("Running hotspot: " + str(self.ifconfig))
    
    
    @property
    def ifconfig(self):
        return self._ifc.ifconfig()
    
    
    def http_get_json(self, url):
        log("HTTP GET: " + url)
        import urequests
        
        for i in range(10):
            try:
                return urequests.get(url).json()
            except OSError as e:
                if e.errno in (ECONNABORTED, ENOBUFS):
                    sleep_ms(100)
            except ValueError as e:
                raise JsonError(e)
        
        raise RuntimeError('Connection failed')
    
    
    def disconnect(self):
        WLAN(STA_IF).active(False)
        WLAN(AP_IF).active(False)
        self._ifc = None
