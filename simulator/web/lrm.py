from config import location, Location
import web


@web.webpage_handler(__name__)
def www(page, args):
    name = args['name']

    for i in range(len(location)):
        if location[i].name == name:
            location.remove(location[i])
            Location.flush()
            break

    web.index(page)
