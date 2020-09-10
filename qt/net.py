import gc


class Wifi:
    def __init__(self, ssid, bssid):
        __slots__  = ('ssid', 'bssid')
        self.ssid  = ssid
        self.bssid = bssid


class Connection:
    def __init__(self):
        from config import connection
        self.country  = connection[0].country
        self.location = connection[0].location
        self.nets     = [ Wifi('mynet1', b'aaaaaa'), Wifi('mynet2', b'bbbbbb') ]
    
    @property
    def ifconfig(self):
        return ('192.168.1.254', '255.255.255.0', '192.168.1.255')
    
    def http_get_json(self, url):
        print("HTTP GET: " + url)
        import requests
        return requests.get(url).json()
    
    def disconnect(self):
        pass
