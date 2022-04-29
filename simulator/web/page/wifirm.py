from db import connection, Connection
import web


@web.action_handler(__name__)
def www(page, args):
    bssid = web.bssid2bytes(args['bssid'])
    connections = connection.CONNECTIONS

    for i in range(len(connections)):
        if connections[i].bssid == bssid:
            connections.remove(connection[i])
            connection.CONNECTIONS = connections
            break

    web.index(page)
