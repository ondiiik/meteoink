from config import ui

if 'CZ' == ui.language:
    from .lang_cz import *
else:
    from .lang_en import *