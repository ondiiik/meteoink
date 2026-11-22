from ulogging import getLogger

logger = getLogger(__name__)

from config import behavior
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args, error=None):
    page.heading(2, trn("Edit remote display key"))

    if error:
        page += f'<p style="color:red">{error}</p>'

    page += f"<p>{trn('Key has 64 hexadecimal characters (256 bits). The same key has to be set on remote display server.')}</p>"

    with page.form("dkeyset") as form:
        form.input(trn("Key"), "key", behavior.get("display_key", ""))
        form.checkbox(trn("Generate new random key"), "gen")
