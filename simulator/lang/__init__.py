from ulogging import getLogger

logger = getLogger(__name__)

from db import api

if "CZ" == api.LANGUAGE:
    from .lang_cz import *
else:
    from .lang_en import *
