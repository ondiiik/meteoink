from config import temp
from log import dump_exception


def page(web):
    try:
        l = float(web.args['ihi']), float(web.args['ohi']), float(web.args['olo'])
        temp.indoor_high, temp.outdoor_high, temp.outdoor_low = l
        temp.flush()
    except Exception as e:
        dump_exception('WEB error:', e)
    
    return True
