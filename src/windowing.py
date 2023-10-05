from datetime import datetime, timedelta
from enum import Enum

class IntervalType(Enum):
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"
    SECONDS = "seconds"

class Window():
    def __init__(self, interval_length=1, interval_type=None, now=None):
        _check_interval_length(interval_length)
        if interval_type is None:
            raise ValueError("interval_type must not be None")
        if now is None:
            now = datetime.now()

        self.interval_length = interval_length
        self.interval_type = interval_type
        self.start, self.stop = get_current_window(interval_length, interval_type, now)
    
    @property
    def next_window(self):
        return Window(self.interval_length, self.interval_type, self.stop)
    
    @property
    def previous_window(self):
        start, stop = get_previous_window(self.interval_length, self.interval_type, self.start)
        return Window(self.interval_length, self.interval_type, start)

def get_next_window(interval_length, interval_type, now=None):
    _check_interval_length(interval_length)
    current_window = get_current_window(interval_length, interval_type, now)
    days, hours, minutes = 0, 0, 0

    if interval_type == IntervalType.DAYS:
        days = interval_length
    elif interval_type == IntervalType.HOURS:
        hours = interval_length
    if interval_type == IntervalType.MINUTES:
        minutes = interval_length
    td = timedelta(days=days, hours=hours, minutes=minutes)
    return(current_window[0] + td, current_window[1] + td)
    
def get_current_window(interval_length, interval_type, now=None):
    _check_interval_length(interval_length)
    
    if now == None:
        now = datetime.now()

    if interval_type == IntervalType.MINUTES:
            hours = interval_length // 60
            start = now
            if interval_length < 60:
                minute = (now.minute // interval_length) * interval_length
                if minute >= 60:
                    start = now.replace(minute=0, second=0, microsecond=0)
                else:
                    start = now.replace(minute=minute, second=0, microsecond=0)
            else:
                start = now.replace(minute=0, second=0, microsecond=0)
            stop_time = start + timedelta(minutes=interval_length)
            stop = stop_time.replace(second=0, microsecond=0)
            return (start, stop)
    
    if interval_type == IntervalType.HOURS:
        start = now.replace(hour=now.hour, minute=0, second=0, microsecond=0)

        days = interval_length // 24
        
        stop_time = now + timedelta(days = days, hours=interval_length)
        stop = stop_time.replace(minute=0, second=0, microsecond=0)
        return (start, stop)
        
    if interval_type == IntervalType.DAYS:
        start = now.replace(day=now.day, hour=0, minute=0, second=0, microsecond=0)
        
        stop_time = now + timedelta(days = interval_length)
        stop = stop_time.replace(hour=0, minute=0, second=0, microsecond=0)
        return (start, stop)

def get_previous_window(interval_length, interval_type, now=None):
    _check_interval_length(interval_length)
    current_window = get_current_window(interval_length, interval_type, now)
    days, hours, minutes = 0, 0, 0

    if interval_type == IntervalType.DAYS:
        days = interval_length
    elif interval_type == IntervalType.HOURS:
        hours = interval_length
    if interval_type == IntervalType.MINUTES:
        minutes = interval_length
    td = timedelta(days=days, hours=hours, minutes=minutes)
    return(current_window[0] - td, current_window[1] - td)

def _check_interval_length(interval_length):
    if not isinstance(interval_length, int):
        raise TypeError("interval_count must be an integer")

    if interval_length <= 0:
        raise ValueError("interval_count must be greater than zero")