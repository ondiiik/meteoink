from config import location, Location, connection
import web


@web.action_handler(__name__)
def www(page, args):
    name = args['name']

    for i in range(len(location)):
        if location[i].name == name:
            for j in range(len(connection)):
                if connection[j].location == i:
                    connection[j].location = 0

            location.remove(location[i])
            Location.flush()
            break

    web.index(page)
