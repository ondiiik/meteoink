import              socket
from utime   import sleep_ms
from uerrno  import ECONNRESET, ENOTCONN, EAGAIN
from log     import dump_exception
from var     import write
from machine import deepsleep
from buzzer  import play
from log     import log
from lang    import trn


class Server():
    def __init__(self, net):
        self.net    = net
        self.client = None
        self.args   = {}
        self.page  = ''
    
    
    def run(self):
        # Open TCP socket for listening
        addr = socket.getaddrinfo('0.0.0.0', 5555)[0][-1]
        sck  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sck.bind(addr)
        sck.setblocking(False)
        sck.listen(1)
        
        log('Web server listening on', addr)
        
        # Wait for incomming connection
        while True:
            while True:
                try:
                    self.client, addr = sck.accept()
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
                request   = self.client.makefile('rwb', 0)
                self.args = {}
                
                while True:
                    line = request.readline()
                    
                    if not line or line == b'\r\n':
                        break
                    
                    line = line.decode()
                    log('LINE', line.rstrip())
                    
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
                            self.args[key[0]] = key[1].replace('%3A', ':').replace('+', ' ').replace('%2B', '+')
                            
                        log('ARGS', self.args)
            except Exception as e:
                dump_exception('WEB page failed ?!', e)
                self.page = 'index'
            
            self._ack()
            self._send_page()
            self.client = None
    
    
    def write(self, txt):
        retry = True
        
        while retry:
            try:
                self.client.send(txt.encode())
                retry = False
            except OSError as e:
                dump_exception('WEB page write failed ?!', e)
                
                if e.errno in (ENOTCONN, ECONNRESET):
                    self._restart('Disconnected - restarting !!!')
                
                raise e
    
    
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
        return '<button type="button" onclick="location.href=\'{}{}\'">{}</button>'.format(url, Server.mk_args(args_list), caption)
    
    
    @staticmethod
    def button_enable(flag, url):
        return Server.button(trn['Disable' if flag else 'Enable'],
                             url + ('d' if flag else 'e'))
    
    
    @staticmethod
    def form_head(page):
        return '<form action="/{}">{}'.format(page, Server.table_head(('', '')))
    
    
    @staticmethod
    def form_tail(label_submit = 'Submit', label_cancel = 'Cancel'):
        return '{}<br><br><input type="submit" value="{}"><button><a href="/">{}</a></button></form>'.format(Server.table_tail(), label_submit, label_cancel)
    
    
    @staticmethod
    def form_spacer():
        return Server.table_row(('', ''), 1)
    
    
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
        self.client.send(b'HTTP/1.0 200 OK\nContent-type: text/html\n\n')
        
        
    def _head(self):
        self.write('<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><title>{0}</title></head><body><h1>{0}</h1>'.format(trn['Meteostation']))
        
        
    def _tail(self):
        self.client.send(b'</body></html>')
    
    
    @staticmethod
    def _restart(msg):
        log(msg)
        play((2093, 30), 120, (1568, 30), 120, (1319, 30), 120, (1047, 30))
        write('mode', (1,), force = True)
        deepsleep(1)
