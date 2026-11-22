from ulogging import getLogger, dump_exception

logger = getLogger(__name__)

from lang import trn
from version import VERSION
from os import stat
from micropython import const
from net import bytes2bssid
from utime import ticks_ms
import gc

try:
    from utime import ticks_diff
except ImportError:  # Simulator

    def ticks_diff(a, b):
        return a - b


try:
    from network import WLAN, AP_IF
except ImportError:  # Simulator
    WLAN = AP_IF = None
from .microweb.microWebSrv import MicroWebSrv


SPACES = const(4)
CONN_RETRY_CNT = const(6)
actions = dict()


class WebServer:
    net = None
    wdt = None

    def __init__(self, net, wdt):
        type(self).wdt = wdt
        type(self).net = net
        self.client = None
        self.args = {}
        self.page = ""
        self.wdt.feed()

    def run(self):
        self.wdt.feed()
        logger.info("Starting WEB server")
        www_dir = "/www"
        server = MicroWebSrv(webPath=f"{www_dir}/", port=5555)
        server.MaxWebSocketRecvLen = 256
        server.WebSocketThreaded = False
        server.IdleCallback = self._idle
        self._stations = set()
        self._heartbeat = ticks_ms()
        self.wdt.feed()
        server.Start()

    def _idle(self):
        # Server waits for connection - keep watchdog happy and report what
        # is happening around (helps with diagnostics of connection troubles)
        self.wdt.feed()

        try:
            stations = set(bytes2bssid(s[0]) for s in WLAN(AP_IF).status("stations"))
        except Exception:
            stations = self._stations  # Not supported (e.g. simulator)

        for mac in stations - self._stations:
            logger.info(f"WiFi client joined hotspot: {mac}")
        for mac in self._stations - stations:
            logger.info(f"WiFi client left hotspot: {mac}")
        self._stations = stations

        now = ticks_ms()
        if ticks_diff(now, self._heartbeat) >= 30000:
            self._heartbeat = now
            mem = gc.mem_free() if hasattr(gc, "mem_free") else "?"
            logger.info(
                f"Waiting for connections ({len(stations)} WiFi clients, free mem {mem} B)"
            )


def button(caption, action, args_list={}):
    ret = f'<form method="post" class="inline"><input type="hidden" name="action" value="{action}">'

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
        self.page += f'<label for="{self.name}">{self.label}</label><select name="{self.name}" id="{self.name}">'
        return self

    def __exit__(self, type, value, traceback):
        self.page += "</select>"

    def option(self, value, name, selected=False):
        self.page += (
            f'<option value="{value}"{" selected" if selected else ""}>{name}</option>'
        )


class _Table:
    def __init__(self, page, cells, table_attr="", heading_attr=""):
        self.page = page
        self.cells = cells
        self.table_attr = table_attr
        self.heading_attr = heading_attr

    def __enter__(self):
        self.page += f"<table {self.table_attr}><thead>"

        if not self.cells is None:
            self.page += "<tr>"

            for cell in self.cells:
                self.page += f"<th {self.heading_attr}>{cell}</th>"

            self.page += "</tr>"

        self.page += "</thead><tbody>"
        return self

    def __exit__(self, type, value, traceback):
        self.page += "</tbody></table>"

    def row(self, cells, space=0):
        self.page += "<tr>"
        space = "&nbsp;" * space

        for cell in cells:
            self.page += f"<td>{cell}{space}</td>"

        self.page += "</tr>"


class _Form(_Table):
    def __init__(
        self, page, action, label_submit=trn("Submit"), label_cancel=trn("Cancel")
    ):
        super().__init__(page, ("", ""), 'class="form"')
        self.action = action
        self.label_submit = label_submit
        self.label_cancel = label_cancel

    def __enter__(self):
        self.page += f'<form  method="post"><input type="hidden" name="action" value="{self.action}">'
        super().__enter__()
        return self

    def __exit__(self, type, value, traceback):
        super().__exit__(type, value, traceback)
        self.page += f'<div class="form-buttons"><input type="submit" class="button" value="{self.label_submit}"><button class="button"><a href="/">{self.label_cancel}</a></button></div></form>'

    def label(self, txt, var, dfl="", tp="text", space=4):
        self.row(
            (
                f"<label>{txt}</label>",
                f'<input type="{tp}" value="{dfl}" disabled="1"><input type="hidden" name="{var}" value="{dfl}" />'
            ),
            space,
        )

    def input(self, txt, var, dfl="", tp="text", space=4):
        self.row(
            (
                f"<label>{txt}</label>",
                f'<input type="{tp}" id="{var}" name="{var}" value="{dfl}">',
            ),
            space,
        )

    def variable(self, var, val):
        self.page += f'<tr class="hidden-row"><td><input type="hidden" id="{var}" name="{var}" value="{val}" /></td></tr>'

    def checkbox(self, txt, var, checked=False, space=4):
        self.row(
            (
                f"<label>{txt}</label>",
                f'<input type="checkbox" id="{var}" name="{var}"{" checked" if checked else ""}>',
            ),
            space,
        )

    def spacer(self):
        self.page += '<tr class="spacer"><td></td></tr>'


# Static files are cached by browser "forever", so version of style sheet is
# part of its URL - any change of firmware or of the file itself loads it again
try:
    _st = stat("/www/microweb.css")
    _CSS_VER = f"{VERSION}-{_st[6]}-{_st[8]}"
    del _st
except OSError:
    _CSS_VER = VERSION


class Page:
    def __init__(self, response):
        # Page is collected from parts and joined at once at the end (appending
        # to one big string copies and re-hashes whole string each time, which
        # is very slow in MicroPython)
        self._parts = []
        self._t0 = ticks_ms()
        self.response = response

    @property
    def doc(self):
        if len(self._parts) > 1:
            self._parts = ["".join(self._parts)]
        return self._parts[0] if self._parts else ""

    def __enter__(self):
        self._parts.append(f'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"><title>Meteostation</title><link rel="stylesheet" href="microweb.css?v={_CSS_VER}"></head><body>')
        return self

    def __exit__(self, type, value, traceback):
        self._parts.append("</body></html>")
        self.response.WriteResponseOk(
            headers=None,
            contentType="text/html",
            contentCharset="UTF-8",
            content=self.doc,
        )

    def __str__(self):
        return self.doc

    def __iadd__(self, other):
        self._parts.append(other)
        return self

    def table(self, cells, table_attr="", heading_attr=""):
        return _Table(self, cells, table_attr, heading_attr)

    def form(self, url, label_submit=trn("Submit"), label_cancel=trn("Cancel")):
        return _Form(self, url, label_submit, label_cancel)

    def select(self, label, name):
        return _Select(self, label, name)

    def heading(self, level, txt):
        logger.info(f"Page section '{txt}' started at {ticks_diff(ticks_ms(), self._t0)} ms")
        self._parts.append(f"<h{level}>{txt}</h{level}>")

    def br(self, cnt=1):
        self._parts.append("<br>" * cnt)

    def button(self, caption, url, args_list={}):
        self._parts.append(button(caption, url, args_list))


def webpage_handler(name, method="POST"):
    decorate = MicroWebSrv.route(name2page(name), method)

    def builder(fn):
        @decorate
        def wrapper(client, response):
            WebServer.wdt.feed()
            t0 = ticks_ms()
            args = (
                client.ReadRequestPostedFormData()
                if method == "POST"
                else client.GetRequestQueryParams()
            )
            logger.info(f"Page {name}: args {list(args)} read in {ticks_diff(ticks_ms(), t0)} ms")
            with Page(response) as page:
                try:
                    fn(page, args)
                except Exception as e:
                    dump_exception(f"Page {name} failed", e)
                    raise
                logger.info(f"Page {name}: {len(page.doc)} chars built in {ticks_diff(ticks_ms(), t0)} ms")
            WebServer.wdt.feed()

        return wrapper

    return builder


def action_handler(name):
    def builder(fn):
        actions[name2page(name)[1:]] = fn
        return fn

    return builder


def button_enable(flag, url):
    return button(trn("Disable" if flag else "Enable"), url + ("d" if flag else "e"))


def name2page(name):
    name = name.split(".")[-1]
    return "/" if name == "index" else f"/{name}"


def send_page(client, response, page):
    content = "".join(page(client, response))
    response.WriteResponseOk(
        headers=None, contentType="text/html", contentCharset="UTF-8", content=content
    )


from .page.index import www, index
from .page.alertbugd import www
from .page.alertbuge import www
from .page.alerttempd import www
from .page.alerttempe import www
from .page.apiedt import www
from .page.apiset import www
from .page.battedt import www
from .page.battset import www
from .page.dkeyedt import www
from .page.dkeyset import www
from .page.langedt import www
from .page.languse import www
from .page.locdlt import www
from .page.locedt import www
from .page.locmake import www
from .page.locnew import www
from .page.locrm import www
from .page.locset import www
from .page.passedt import www
from .page.passset import www
from .page.refredt import www
from .page.refrset import www
from .page.reset import www
from .page.ssidedt import www
from .page.ssidset import www
from .page.summertd import www
from .page.summerte import www
from .page.tempedt import www
from .page.tempset import www
from .page.variantedt import www
from .page.variantuse import www
from .page.wifidlt import www
from .page.wifiedt import www
from .page.wifimake import www
from .page.wifinew import www
from .page.wifirm import www
from .page.wifiset import www, wifiset
from .page.wifiuse import www
from .page.zzz import www
