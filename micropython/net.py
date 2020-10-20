import heap


class Wifi:
    __slots__  = ('ssid', 'bssid')
    
    def __init__(self, ssid, bssid):
        self.ssid  = ssid
        self.bssid = bssid


class Connection:
    __slots__ = ('config', 'nets', 'is_hotspot', '_ifc')
    
    def __init__(self):
        # Scan networks in surrounding
        from jumpers import hotspot
        from network import WLAN, STA_IF
        
        self._ifc = WLAN(STA_IF)
        heap.refresh()
        
        if not self._ifc.active(True):
            raise RuntimeError("WiFi activation failed")
        
        sc        = self._ifc.scan()
        self.nets = []
        
        for n in sc:
            self.nets.append(Wifi(n[0].decode(), n[1]))
        
        self._ifc.active(False)
        
        # Start requested variant of connection
        if hotspot():
            self._hotspot()
        else:
            self._attach()
    
    
    def _attach(self):
        from network import WLAN, STA_IF
        from config  import connection
        from utime   import sleep
        
        # Activate WiFi interface
        self._ifc = WLAN(STA_IF)
        heap.refresh()
        
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
            raise RuntimeError("No know WiFi found!")
        
        self.config = network
        
        self._ifc.connect(network.ssid, network.passwd, bssid = network.bssid)
        
        for i in range(8):
            if self._ifc.isconnected():
                heap.refresh()
                print("Connected: " + str(self.ifconfig))
                self.is_hotspot = False
                return
            
            heap.refresh()
            sleep(1)
            
        raise RuntimeError("Wifi connection refused")
    
    
    def _hotspot(self):
        # Create hotspot to be able to attach by FTP and configure meteostation
        from network import WLAN, AP_IF
        from config  import hotspot
        from utime   import sleep
        
        self._ifc = WLAN(AP_IF)
        self._ifc.active(True)
        self._ifc.config(essid = hotspot.ssid, password = hotspot.passwd, authmode = 3)
        
        while self._ifc.active() == False:
            sleep(1)
        
        self.is_hotspot = True
    
    
    @property
    def ifconfig(self):
        return self._ifc.ifconfig()
    
    
    def http_get_json(self, url):
        print("HTTP GET: " + url)
        import urequests
        return urequests.get(url).json()
    
    
    def disconnect(self):
        from network import WLAN, STA_IF, AP_IF
        WLAN(STA_IF).active(False)
        WLAN(AP_IF).active(False)
        self._ifc = None
