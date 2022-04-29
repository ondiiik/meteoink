from db import location, connection
import web


@web.action_handler(__name__)
def www(page, args):
    name = args['name']
    locations = location.LOCATIONS
    connections = connection.CONNECTIONS

    for i in range(len(locations)):
        if locations[i].name == name:
            for j in range(len(connections)):
                if connections[j].location == i:
                    connections[j].location = 0

            locations.remove(locations[i])
            location.LOCATIONS = locations
            break

    web.index(page)
