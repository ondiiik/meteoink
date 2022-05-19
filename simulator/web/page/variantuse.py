from ulogging import getLogger
logger = getLogger(__name__)

from db import api
import web


@web.action_handler(__name__)
def www(page, args):
    api.VARIANT = int(args['v'])
    web.index(page)
