from utime import localtime
from config import time


class Time():
    def __init__(self, timezone):
        wt_offset = 3600 * time.winter
        self.time_offset = -946670400 - wt_offset - timezone

    def get_date_time(self, unix_time):
        return localtime(unix_time + self.time_offset)
