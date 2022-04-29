from ulogging import getLogger
logger = getLogger(__name__)

from db import ui

if 'CZ' == ui.LANGUAGE:
    from .lang_cz import *
else:
    from .lang_en import *
