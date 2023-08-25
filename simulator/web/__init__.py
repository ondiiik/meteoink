from ulogging import getLogger

logger = getLogger(__name__)

from lang import trn
from micropython import const
from net import bytes2bssid
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
        self.wdt.feed()
        server.Start()


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
        self.page += '<label for="{1}">{0}</label><select name="{1}" id="{1}">'.format(
            self.label, self.name
        )
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
            self.page += "<td>{}{}</td>".format(cell, space)

        self.page += "</tr>"


class _Form(_Table):
    def __init__(
        self, page, action, label_submit=trn("Submit"), label_cancel=trn("Cancel")
    ):
        super().__init__(page, ("", ""))
        self.action = action
        self.label_submit = label_submit
        self.label_cancel = label_cancel

    def __enter__(self):
        self.page += f'<form  method="post"><input type="hidden" name="action" value="{self.action}">'
        super().__enter__()
        return self

    def __exit__(self, type, value, traceback):
        super().__exit__(type, value, traceback)
        self.page += f'<br><br><input type="submit" class="button" value="{self.label_submit}"><button class="button"><a href="/">{self.label_cancel}</a></button></form>'

    def label(self, txt, var, dfl="", tp="text", space=4):
        self.row(
            (
                f"<label>{txt}</label>",
                '<input type="{3}" value="{2}" disabled="1"><input type="hidden" name="{0}" value="{2}" />'.format(
                    var, txt, dfl, tp
                ),
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
        self.row(
            (f'<input type="hidden" id="{var}" name="{var}" value="{val}" />',),
            0,
        )

    def checkbox(self, txt, var, checked=False, space=4):
        self.row(
            (
                f"<label>{txt}</label>",
                f'<input type="checkbox" id="{var}" name="{var}"{" checked" if checked else ""}>',
            ),
            space,
        )

    def spacer(self):
        self.row(("", ""), 1)


class Page:
    def __init__(self, response):
        self.doc = ""
        self.response = response

    def __enter__(self):
        self.doc += '<!DOCTYPE html><html><head><link rel="stylesheet" href="microweb.css"></head><body>'
        return self

    def __exit__(self, type, value, traceback):
        self.doc += "</body></html>"
        self.response.WriteResponseOk(
            headers=None,
            contentType="text/html",
            contentCharset="UTF-8",
            content=self.doc,
        )

    def __str__(self):
        return self.doc

    def __iadd__(self, other):
        self.doc += other
        return self

    def table(self, cells, table_attr="", heading_attr=""):
        return _Table(self, cells, table_attr, heading_attr)

    def form(self, url, label_submit=trn("Submit"), label_cancel=trn("Cancel")):
        return _Form(self, url, label_submit, label_cancel)

    def select(self, label, name):
        return _Select(self, label, name)

    def heading(self, level, txt):
        self.doc += "<h{0}>{1}</h{0}>".format(level, txt)

    def br(self, cnt=1):
        self.doc += "<br>" * cnt

    def button(self, caption, url, args_list={}):
        self.doc += button(caption, url, args_list)


def webpage_handler(name, method="POST"):
    decorate = MicroWebSrv.route(name2page(name), method)

    def builder(fn):
        @decorate
        def wrapper(client, response):
            WebServer.wdt.feed()
            args = (
                client.ReadRequestPostedFormData()
                if method == "POST"
                else client.GetRequestQueryParams()
            )
            with Page(response) as page:
                fn(page, args)
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
