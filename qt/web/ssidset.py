from config import hotspot


def page(web):
    hotspot.ssid = web.args['id']
    hotspot.flush()
    return True
