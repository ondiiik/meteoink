from ulogging import getLogger
logger = getLogger(__name__)

from machine import reset
from .base import init, write, modules

need_reset = False
need_reset |= init('alert', {'ALREADY_TRIGGERED': 0})
need_reset |= init('display', {'DISPLAY_STATE': 0})

if need_reset:
    reset()
