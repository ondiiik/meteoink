from config import ui
from log    import dump_exception


def page(web):
    try:
        ui.apikey = web.args['key']
        ui.flush()
    except Exception as e:
        dump_exception('WEB error:', e)
    
    yield web.index
