from config import alert
import web


@web.action_handler(__name__)
def www(page, args):
    if not alert.temp_balanced:
        alert.temp_balanced = True
        alert.flush()

    web.index(page)
