from config import ui
from log    import dump_exception


def page(web):
    try:
        l                  = int(web.args['t']), (int(web.args['b']), int(web.args['e']))
        ui.refresh, ui.dbl = l
        ui.flush()
    except Exception as e:
        dump_exception('WEB error:', e)
    
    return True
