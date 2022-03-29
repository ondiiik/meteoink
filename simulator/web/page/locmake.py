from config import location, Location
import web


@web.action_handler(__name__)
def www(page, args):
    gps = [float(ll[:-1] if ll[-1] in ('N', 'E') else ll) for ll in args['gps'].split(',')]
    location.append(Location(args['name'], gps[0], gps[1]))
    Location.flush()

    web.index(page)
