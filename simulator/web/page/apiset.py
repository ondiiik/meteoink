from db import api
import web


@web.action_handler(__name__)
def www(page, args):
    api.APIKEY = args['key']
    web.index(page)
