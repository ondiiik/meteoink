from ulogging import getLogger

logger = getLogger(__name__)

from config import behavior
from lang import trn
from os import urandom
import web


@web.action_handler(__name__)
def www(page, args):
    if "gen" in args:
        key = urandom(32).hex()
        logger.info("New random remote display key generated")
    else:
        # Be tolerant to copy-paste formatting (spaces, colons, upper case)
        key = "".join(c for c in args.get("key", "") if c not in " :-\t").lower()

        if len(key) != 64 or any(c not in "0123456789abcdef" for c in key):
            logger.warning("Invalid remote display key entered")
            web.actions["dkeyedt"](
                page,
                args,
                trn("Invalid key - it has to be 64 hexadecimal characters (0-9, a-f)."),
            )
            return

    behavior["display_key"] = key
    behavior.flush()
    logger.info("Remote display key changed")
    web.index(page)
