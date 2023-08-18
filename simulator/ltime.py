from config import time
from utime import localtime
from ulogging import getLogger

logger = getLogger(__name__)


class Time:
    def __init__(self, timezone):
        offset = -946674000 if time["winter"] else -946670400
        self.time_offset = offset - timezone

    def get_date_time(self, unix_time):
        return localtime(unix_time + self.time_offset)
