from ulogging import getLogger

logger = getLogger(__name__)

from config import api

if "cz" == api["language"]:
    from .lang_cz import *
else:
    from .lang_en import *
