from buzzer      import play
from gc          import collect
from lang        import trn
from log         import dump_exception
from log         import log
from machine     import deepsleep
from micropython import const
from uerrno      import ECONNRESET, ENOTCONN, EAGAIN, ETIMEDOUT
from uio         import BytesIO
from utime       import sleep_ms
from var         import write
import                  socket


SPACES         = const(4)
CONN_RETRY_CNT = const(6)


class Server():
    def __init__(self, net, wdt):
        self.wdt    = wdt
        self.net    = net
        self.client = None
        self.args   = {}
        self.page   = ''
        self.wdt.feed()
    
    
    def run(self):
        # Open TCP socket for listening
        self.wdt.feed()
        addr = socket.getaddrinfo('0.0.0.0', 5555)[0][-1]
        sck  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.wdt.feed()
        sck.bind(addr)
        self.wdt.feed()
        sck.setblocking(False)
        self.wdt.feed()
        sck.listen(1)
        self.wdt.feed()
        
        log('Web server listening on', addr)
        
        # Wait for incoming connection
        while True:
            self.wdt.feed()
            
            while True:
                try:
                    self.client, addr = sck.accept()
                    self.wdt.feed()
                    break
                except OSError as e:
                    if e.errno == EAGAIN:
                        sleep_ms(100)
                    elif e.errno == 23: # Out of memory - restart server
                        self._restart('Low memory - restart !!!')
                    else:
                        dump_exception('Socket accept failed ?!', e)
                    pass
            
            self.client.settimeout(8.0)
            log('Accepted client from', addr)
            
            
            try:
                # Parse HTTP request
                self.wdt.feed()
                request   = self.client.makefile('rwb', 0)
                self.args = {}
                
                while True:
                    self.wdt.feed()
                    
                    try:
                        line = request.readline()
                        self.wdt.feed()
                    except OSError as e:
                        if e.errno == ETIMEDOUT:
                            log('Timeout - interrupt')
                            break
                        
                        raise e
                    
                    
                    if not line or line == b'\r\n':
                        break
                    
                    line = line.decode()
                    log('LINE', line.rstrip())
                    self.wdt.feed()
                    
                    # Check for GET file and args
                    if line.startswith('GET '):
                        line = line.split()
                        
                        # Parse GET request like '/page?arg1=n1&arg2=n2&...'
                        if len(line) < 3:
                            continue
                        
                        log('REQ', line[1])
                        if not line[1].startswith('/'):
                            continue
                        
                        line = line[1][1:].split('?', 1)
                        log('SPLIT', line)
                        
                        self.page = line[0]
                        log('PAGE', self.page)
                        
                        if len(line) < 2:
                            continue
                        
                        line = line[1].split('&')
                        
                        if len(line[0]) < 1:
                            continue
                        if line[0] == '':
                            continue
                        
                        for key in line:
                            log(key)
                            key = key.split('=', 1)
                            
                            p = key[1].replace('+', ' ').split('%')
                            t = bytearray(p[0].encode())
                            
                            for k in p[1:]:
                                t.append(int(k[0:2], 16))
                                t.extend(k[2:].encode())
                            
                            self.args[key[0]] = t.decode()
                            
                        log('ARGS', self.args)
            except Exception as e:
                dump_exception('WEB page failed ?!', e)
                self.page = 'index'
            
            try:
                self._ack()
                self._send_page()
                self.client = None
            except OSError as e:
                if e.errno == ENOTCONN:
                    log('Connection dropped')
    
    
    def write(self, txt):
        if isinstance(txt, str):
            txt = txt.encode()
        
        for retry in range(CONN_RETRY_CNT):
            try:
                self.wdt.feed()
                self.client.send(txt)
                self.wdt.feed()
                collect()
                self.wdt.feed()
                return
            except OSError as e:
                log('ECONNRESET -> retry')
                if e.errno == ECONNRESET:
                    continue
                
                raise e
        
        raise RuntimeError('Connection broken')
    
    
    @staticmethod
    def heading(level, txt):
        return '<h{0}>{1}</h{0}>'.format(level, txt)
    
    
    @staticmethod
    def br(cnt = 1):
        return '<br>' * cnt
    
    
    @staticmethod
    def select_head(label, name):
        return '<label for="{1}">{0}</label><select name="{1}" id="{1}">'.format(label, name)
    
    
    @staticmethod
    def select_option(value, name, selected = False):
        return '<option value="{}"{}>{}</option>'.format(value, ' selected' if selected else '', name)
    
    
    @staticmethod
    def select_tail():
        return '</select>'
    
    
    @staticmethod
    def table_head(cells, table_attr = '', heading_attr = ''):
        ret = '<table {}><thead>'.format(table_attr)
        
        if not cells is None:
            ret += '<tr>'
            
            for cell in cells:
                ret += '<th {}>{}</th>'.format(heading_attr, cell)
            
            ret += '</tr>'
        
        ret += '</thead><tbody>'
        
        return ret
    
    
    @staticmethod
    def table_tail():
        return '</tbody></table>'
    
    
    @staticmethod
    def table_row(cells, space = 0):
        ret   = '<tr>'
        space = '&nbsp;' * space
        
        for cell in cells:
            ret += '<td>{}{}</td>'.format(cell, space)
        
        ret += '</tr>'
        
        return ret
        
        
        
    @staticmethod
    def mk_args(args_list):
        if args_list is None:
            ret = ''
        else:
            ret = None
            for arg in args_list:
                if ret is None:
                    ret = '?'
                else:
                    ret += '&'
                
                if arg[1] is None:
                    ret += '{}'.format(arg[0])
                else:
                    ret += '{}={}'.format(arg[0], arg[1])
        
        return ret
    
    
    @staticmethod
    def button(caption, url, args_list = None):
        return '<button class="button" onclick="location.href=\'{}{}\'">{}</button>'.format(url, Server.mk_args(args_list), caption)
    
    
    @staticmethod
    def button_enable(flag, url):
        return Server.button(trn['Disable' if flag else 'Enable'],
                             url + ('d' if flag else 'e'))
    
    
    @staticmethod
    def form_head(page):
        return '<form action="/{}">{}'.format(page, Server.table_head(('', '')))
    
    
    @staticmethod
    def form_tail(label_submit = trn['Submit'], label_cancel = trn['Cancel']):
        return '{}<br><br><input type="submit" class="button" value="{}"><button class="button"><a href="/">{}</a></button></form>'.format(Server.table_tail(), label_submit, label_cancel)
    
    
    @staticmethod
    def form_spacer():
        return Server.table_row(('', ''), 1)
    
    
    @staticmethod
    def form_variable(var, val):
        return Server.table_row(('<input type="hidden" id="{0}" name="{0}" value="{1}" />'.format(var, val),), 0)
    
    
    @staticmethod
    def form_input(txt, var, dfl = '', tp = 'text', space = 4):
        return Server.table_row(('<label>{}</label>'.format(txt),
                                 '<input type="{3}" id="{0}" name="{0}" value="{2}">'.format(var, txt, dfl, tp)),
                                 space)
    
    
    @staticmethod
    def form_label(txt, var, dfl = '', tp = 'text', space = 4):
        return Server.table_row(('<label>{}</label>'.format(txt),
                                 '<input type="{3}" value="{2}" disabled="1"><input type="hidden" name="{0}" value="{2}" />'.format(var, txt, dfl, tp)),
                                 space)
    
    
    def _send_page(self):
        self._head()
        self.process()
        self._tail()
        
        
    def _ack(self):
        self.wdt.feed()
        self.client.send(b'HTTP/1.0 200 OK\nContent-type: text/html\n\n')
        self.wdt.feed()
        
        
    def _head(self):
        self.write('<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8; width=device-width; initial-scale=1"><title>{0}</title></head><body><h1>{0}</h1>'.format(trn['Meteostation']))
        self.write('<style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; font-size: 16px;}')
        self.write('h1{color: #0F3376;}')
        self.write('p{font-size: 1.5rem;}')
        self.write('.button{display: inline-block; background-color: #0074d9; border: none; border-radius: 4px; color: white; padding: 6px 20px; text-decoration: none; font-size: 14px; margin: 2px; cursor: pointer;}')
        self.write('.butt_on{background-color: #42f486;}')
        self.write('.butt_off{background-color: #4286f4;}')
        self.write('</style>')
        
        
    def _tail(self):
        self.wdt.feed()
        self.client.send(b'</body></html>')
        self.wdt.feed()
    
    
    @staticmethod
    def _restart(msg):
        self.wdt.feed()
        log(msg)
        play((2093, 30), 120, (1568, 30), 120, (1319, 30), 120, (1047, 30))
        write('mode', (1,), force = True)
        deepsleep(1)



class WebWriter:
    def __init__(self, web):
        self.s   = BytesIO()
        self.web = web
    
    def write(self, txt):
        if isinstance(txt, str):
            txt = txt.encode()
        
        s   = self.s
        wdt = self.web.wdt
        wdt.feed()
        s.write(txt)
        wdt.feed()
        
        if s.tell() > 1200:
            wdt.feed()
            self.web.write(s.getvalue())
            wdt.feed()
            self.s = BytesIO()
    
    def flush(self):
        if self.s.tell() > 0:
            wdt = self.web.wdt
            wdt.feed()
            self.web.write(self.s.getvalue())
            wdt.feed()
            self.s = BytesIO()



class WebServer(Server):
    class IndexDrawer:
        pass
    
    def __init__(self, net, wdt):
        super().__init__(net, wdt)
        self.writer = WebWriter(self)
        self.last   = ''
        self.index  = WebServer.IndexDrawer()
    
    
    def process(self):
        log('*** PAGE ***', self.page)
        
        if (self.page == '') or (self.last == self.page):
            self.page = 'index'
        
        try:
            page = __import__('web.{}'.format(self.page), None, None, ('page',), 0).page
        except ImportError:
            log('!!! Page {} not found !!!'.format(self.page))
            page = __import__('web.index', None, None, ('page',), 0).page
        
        if not self.last == self.page:
            self.last = self.page
        
        play((1047,30), 120, (1568,30))
        s = BytesIO()
        
        for p in page(self):
            if isinstance(p, WebServer.IndexDrawer):
                for q in __import__('web.index', None, None, ('page',), 0).page(self):
                    self.wdt.feed()
                    self.writer.write(q)
                    self.wdt.feed()
            else:
                self.wdt.feed()
                self.writer.write(p)
                self.wdt.feed()
        
        self.wdt.feed()
        self.writer.flush()
        self.wdt.feed()



def bssid2bytes(bssid):
    b1 = bssid.split(':')
    b2 = []
    for i in range(6):
        b2.append(int(b1[i], 16))
    return bytes(b2)



def bytes2bssid(bssid):
    return ":".join("{:02x}".format(b) for b in bssid)
