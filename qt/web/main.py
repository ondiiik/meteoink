from .           import Server
from buzzer      import play
from micropython import const


SPACES = const(4)


class WebServer(Server):
    def __init__(self, net):
        super().__init__(net)
        self.last  = ''
    
    
    def process(self):
        print('*** PAGE ***', self.page)
        
        if (self.page == '') or (self.last == self.page):
            self.page = 'index'
        
        try:
            page = __import__('web.{}'.format(self.page), None, None, ('page',), 0).page
        except ImportError:
            print('!!! Page {} not found !!!'.format(self.page))
            page = __import__('web.index', None, None, ('page',), 0).page
        
        if not self.last == self.page:
            self.last = self.page
        
        play((1047,30), 120, (1568,30))
        if page(self):
            page = __import__('web.index', None, None, ('page',), 0).page
            page(self)



def bssid2bytes(bssid):
    b1 = bssid.split(':')
    b2 = []
    for i in range(6):
        b2.append(int(b1[i], 16))
    return bytes(b2)


def bytes2bssid(bssid):
    return ":".join("{:02x}".format(b) for b in bssid)
