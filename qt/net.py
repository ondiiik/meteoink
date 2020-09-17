import gc


class Wifi:
    def __init__(self, ssid, bssid):
        __slots__  = ('ssid', 'bssid')
        self.ssid  = ssid
        self.bssid = bssid


class Connection:
    def __init__(self):
        from config import connection
        self.config = connection[0]
        self.nets   = [ Wifi('mynet1', b'aaaaaa'), Wifi('mynet2', b'bbbbbb') ]
    
    @property
    def ifconfig(self):
        return ('192.168.1.254', '255.255.255.0', '192.168.1.255')
    
    def http_get_json(self, url):
        print("HTTP GET: " + url)
        import socket
        from   jread import JsonRead
         
        # Send GET request
        _, _, host, path = url.split('/', 3)
        addr             = socket.getaddrinfo(host, 80)[0][-1]
        s                = socket.socket()
        s.connect(addr)
        s.send(bytes('GET /%s HTTP/1.0\nHost: %s\n\n' % (path, host), 'utf8'))
         
        data0 = ' '
         
        # Strip response head
        while True:
            data1 = s.recv(1)
             
            if data1 == b'\r':
                continue
             
            if data0 == b'\n' and data1 == b'\n':
                break
             
            data0 = data1
         
        # Parse JSON data
        print("Parsing JSON from stream ...")
        j = JsonRead(s) 
        s.close()
        return j.data
#         print("HTTP GET: " + url)
#         import requests
#         return requests.get(url).json()
    
    def disconnect(self):
        pass
