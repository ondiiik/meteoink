from config import temp


def page(web):
    temp.indoor_high  = float(web.args['ihi'])
    temp.outdoor_high = float(web.args['ohi'])
    temp.outdoor_low  = float(web.args['olo'])
    temp.flush()
    return True
