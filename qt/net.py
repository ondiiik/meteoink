from config  import connection
from jumpers import jumpers
from log     import log


class Wifi:
    def __init__(self, ssid, bssid):
        self.ssid  = ssid
        self.bssid = bssid


class Connection:
    def __init__(self):
        self.is_hotspot = jumpers.hotspot
        
        if not self.is_hotspot:
            self.config = connection[0]
        
        self.nets = [ Wifi('mynet1', b'aaaaaa'), Wifi('mynet2', b'bbbbbb') ]
    
    @property
    def ifconfig(self):
        return ('192.168.1.254', '255.255.255.0', '192.168.1.255')
    
    def http_get_json(self, url):
        log("HTTP GET: " + url)
        import urequests
        return urequests.get(url).json()
    
    def disconnect(self):
        pass
