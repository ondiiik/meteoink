from buzzer import play
from gc import collect
from lang import trn
from log import dump_exception
from log import log
from machine import deepsleep
from micropython import const
from uerrno import ECONNRESET, ENOTCONN, EAGAIN, ETIMEDOUT
from uio import BytesIO
from .microweb.microWebSrv import MicroWebSrv
from utime import sleep_ms
from var import write
import socket


SPACES = const(4)
CONN_RETRY_CNT = const(6)


class WebServer:
    net = None

    def __init__(self, net, wdt):
        self.wdt = wdt
        type(self).net = net
        self.client = None
        self.args = {}
        self.page = ''
        self.wdt.feed()

    def run(self):
        # Starting web server
        self.wdt.feed()
        print('[WEB] ', 'Starting WEB server')
        www_dir = '/web/www'
        server = MicroWebSrv(webPath=f'{www_dir}/',
                             port=5555)
        server.MaxWebSocketRecvLen = 256
        server.WebSocketThreaded = False
        self.wdt.feed()
        server.Start()
        # Server is running here - we shall never reach this place


def button(caption, url, args_list={}):
    ret = f'<form method="post" action="{url}" class="inline">'

    for name, value in args_list.items():
        ret += f'<input type="hidden" name="{name}" value="{value}">'

    ret += f'<button class="button">{caption}</button></form>'
    return ret


class _Select:
    def __init__(self, page, label, name):
        self.page = page
        self.label = label
        self.name = name

    def __enter__(self):
        self.page += '<label for="{1}">{0}</label><select name="{1}" id="{1}">'.format(self.label, self.name)
        return self

    def __exit__(self, type, value, traceback):
        self.page += '</select>'

    def option(self, value, name, selected=False):
        self.page += f'<option value="{value}"{" selected" if selected else ""}>{name}</option>'


class _Table:
    def __init__(self, page, cells, table_attr='', heading_attr=''):
        self.page = page
        self.cells = cells
        self.table_attr = table_attr
        self.heading_attr = heading_attr

    def __enter__(self):
        self.page += f'<table {self.table_attr}><thead>'

        if not self.cells is None:
            self.page += '<tr>'

            for cell in self.cells:
                self.page += f'<th {self.heading_attr}>{cell}</th>'

            self.page += '</tr>'

        self.page += '</thead><tbody>'
        return self

    def __exit__(self, type, value, traceback):
        self.page += '</tbody></table>'

    def row(self, cells, space=0):
        self.page += '<tr>'
        space = '&nbsp;' * space

        for cell in cells:
            self.page += '<td>{}{}</td>'.format(cell, space)

        self.page += '</tr>'


class _Form(_Table):
    def __init__(self, page, url, label_submit=trn('Submit'), label_cancel=trn('Cancel')):
        super().__init__(page, ("", ""))
        self.url = url
        self.label_submit = label_submit
        self.label_cancel = label_cancel

    def __enter__(self):
        self.page += f'<form  method="post" action="/{self.url}">'
        super().__enter__()
        return self

    def __exit__(self, type, value, traceback):
        super().__exit__(type, value, traceback)
        self.page += f'<br><br><input type="submit" class="button" value="{self.label_submit}"><button class="button"><a href="/">{self.label_cancel}</a></button></form>'

    def label(self, txt, var, dfl='', tp='text', space=4):
        self.row((f'<label>{txt}</label>',
                  '<input type="{3}" value="{2}" disabled="1"><input type="hidden" name="{0}" value="{2}" />'.format(var, txt, dfl, tp)),
                 space)

    def input(self, txt, var, dfl='', tp='text', space=4):
        self.row((f'<label>{txt}</label>',
                  '<input type="{3}" id="{0}" name="{0}" value="{2}">'.format(var, txt, dfl, tp)),
                 space)

    def variable(self, var, val):
        self.row(('<input type="hidden" id="{0}" name="{0}" value="{1}" />'.format(var, val),), 0)

    def spacer(self):
        self.row(('', ''), 1)


class Page:
    def __init__(self, response):
        self.doc = ''
        self.response = response

    def __enter__(self):
        self.doc += '<!DOCTYPE html><html><head><link rel="stylesheet" href="microweb.css"></head><body>'
        return self

    def __exit__(self, type, value, traceback):
        self.doc += '</body></html>'
        self.response.WriteResponseOk(headers=None,
                                      contentType="text/html",
                                      contentCharset="UTF-8",
                                      content=self.doc)

    def __str__(self):
        return self.doc

    def __iadd__(self, other):
        self.doc += other
        return self

    def table(self, cells, table_attr='', heading_attr=''):
        return _Table(self, cells, table_attr, heading_attr)

    def form(self, url, label_submit=trn('Submit'), label_cancel=trn('Cancel')):
        return _Form(self, url, label_submit, label_cancel)

    def select(self, label, name):
        return _Select(self, label, name)

    def heading(self, level, txt):
        self.doc += '<h{0}>{1}</h{0}>'.format(level, txt)

    def br(self, cnt=1):
        self.doc += '<br>' * cnt

    def button(self, caption, url, args_list={}):
        self.doc += button(caption, url, args_list)


def webpage_handler(name, method='POST'):
    decorate = MicroWebSrv.route(name2page(name), method)

    def builder(fn):
        @decorate
        def wrapper(client, response):
            args = client.ReadRequestPostedFormData() if method == 'POST' else client.GetRequestQueryParams()
            with Page(response) as page:
                fn(page, args)

        return wrapper

    return builder


def button_enable(flag, url):
    return button(trn('Disable' if flag else 'Enable'), url + ('d' if flag else 'e'))


def bssid2bytes(bssid):
    b1 = bssid.split(':')
    b2 = []
    for i in range(6):
        b2.append(int(b1[i], 16))
    return bytes(b2)


def bytes2bssid(bssid):
    return ":".join("{:02x}".format(b) for b in bssid)


def name2page(name):
    name = name.split('.')[-1]
    return '/' if name == 'index' else f'/{name}'


def send_page(client, response, page):
    content = ''.join(page(client, response))
    response.WriteResponseOk(headers=None,
                             contentType="text/html",
                             contentCharset="UTF-8",
                             content=content)


from .index import www, index
from .add import www
from .apikey import www
from .apiset import www
from .dlt import www
from .ed import www
from .lang import www
from .ldlt import www
from .led import www
from .lnew import www
from .lnguse import www
from .low import www
from .lowset import www
from .lrm import www
from .lset import www
from .new import www
from .nloc import www
from .passet import www
from .passwd import www
from .refr import www
from .refrset import www
from .res import www
from .rm import www
from .set import www, set
from .ssid import www
from .ssidset import www
from .swbd import www
from .swbe import www
from .tbad import www
from .tbae import www
from .temp import www
from .tset import www
from .use import www
from .zzz import www
