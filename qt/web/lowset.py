from config import vbat
from log    import dump_exception


def page(web):
    try:
        vbat.low_voltage = max(2.8, min(4.0, float(web.args['v'])))
        vbat.flush()
    except Exception as e:
        dump_exception('WEB error:', e)
    
    yield web.index
