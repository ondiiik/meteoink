from config import location
import web


@web.webpage_handler(__name__)
def www(page, args):
    i = int(args['idx'])
    gps = [float(ll[:-1] if ll[-1] in ('N', 'E') else ll) for ll in args['gps'].split(',')]
    location[i].name = args['name']
    location[i].lat = gps[0]
    location[i].lon = gps[1]
    location[i].flush()

    web.index(page)
