from ulogging import getLogger

logger = getLogger(__name__)

from config import location, connection
import web


@web.action_handler(__name__)
def www(page, args):
    name = args["name"]
    locations = location["locations"]
    connections = connection["connections"]

    for i in range(len(locations)):
        if locations[i]["name"] == name:
            for j in range(len(connections)):
                if connections[j]["location"] == i:
                    connections[j]["location"] = 0
                    connection.flush()

            locations.remove(locations[i])
            location.flush()
            break

    web.index(page)
