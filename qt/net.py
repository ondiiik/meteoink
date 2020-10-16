import gc


class Wifi:
    __slots__ = ('ssid', 'bssid')
    
    def __init__(self, ssid, bssid):
        self.ssid  = ssid
        self.bssid = bssid


class Connection:
    __slots__ = ('config', 'nets', 'is_hotspot', '_ifc')
    
    def __init__(self):
        from config  import connection
        from jumpers import hotspot
        self.is_hotspot = hotspot()
        self.config     = connection[0]
        self.nets       = [ Wifi('mynet1', b'aaaaaa'), Wifi('mynet2', b'bbbbbb') ]
    
    @property
    def ifconfig(self):
        return ('192.168.1.254', '255.255.255.0', '192.168.1.255')
    
    def http_get_json(self, url):
        print("HTTP GET: " + url)
        import urequests
        return urequests.get(url).json()
    
    def disconnect(self):
        pass
