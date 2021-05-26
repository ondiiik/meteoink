from config import vbat, flush


def page(web):
    try:
        vbat.low_voltage = max(2.8, min(4.0, float(web.args['v'])))
        vbat.flush()
    except:
        print('Invalid VBAT value - ', web.args['v'])
    
    return True
