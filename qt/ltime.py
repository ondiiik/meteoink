class Time():
    def __init__(self, timezone):
        self.time_offset = -946670400 - timezone
    
    def get_date_time(self, unix_time):
        from utime import localtime
        return localtime(unix_time + self.time_offset)
