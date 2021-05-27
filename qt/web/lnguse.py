from config import ui
from log    import dump_exception


def page(web):
    try:
        ui.language = web.args['l']
        ui.flush()
    except Exception as e:
        dump_exception('WEB error:', e)
    
    return True
