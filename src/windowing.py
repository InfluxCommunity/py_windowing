from datetime import datetime, timedelta
from enum import Enum

class IntervalType(Enum):
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"
    SECONDS = "seconds"

def get_next_window(interval_count, interval_type, now=None):
    _check_input(interval_count)
    current_window = get_current_window(interval_count, interval_type, now)
    days, hours, minutes = 0, 0, 0

    if interval_type == IntervalType.DAYS:
        days = interval_count
    elif interval_type == IntervalType.HOURS:
        hours = interval_count
    if interval_type == IntervalType.MINUTES:
        minutes = interval_count
    td = timedelta(days=days, hours=hours, minutes=minutes)
    return(current_window[0] + td, current_window[1] + td)
    
def get_current_window(interval_count, interval_type, now=None):
    _check_input(interval_count)
    
    if now == None:
        now = datetime.now()

    if interval_type == IntervalType.MINUTES:
            hours = interval_count // 60
            start = now
            if interval_count < 60:
                minute = (now.minute // interval_count) * interval_count
                if minute >= 60:
                    start = now.replace(minute=0, second=0, microsecond=0)
                else:
                    start = now.replace(minute=minute, second=0, microsecond=0)
            else:
                start = now.replace(minute=0, second=0, microsecond=0)
            stop_time = start + timedelta(minutes=interval_count)
            stop = stop_time.replace(second=0, microsecond=0)
            return (start, stop)
    
    if interval_type == IntervalType.HOURS:
        start = now.replace(hour=now.hour, minute=0, second=0, microsecond=0)

        days = interval_count // 24
        
        stop_time = now + timedelta(days = days, hours=interval_count)
        stop = stop_time.replace(minute=0, second=0, microsecond=0)
        return (start, stop)
        
    if interval_type == IntervalType.DAYS:
        start = now.replace(day=now.day, hour=0, minute=0, second=0, microsecond=0)
        
        stop_time = now + timedelta(days = interval_count)
        stop = stop_time.replace(hour=0, minute=0, second=0, microsecond=0)
        return (start, stop)

def get_previous_window(interval_count, interval_type, now=None):
    _check_input(interval_count)
    current_window = get_current_window(interval_count, interval_type, now)
    days, hours, minutes = 0, 0, 0

    if interval_type == IntervalType.DAYS:
        days = interval_count
    elif interval_type == IntervalType.HOURS:
        hours = interval_count
    if interval_type == IntervalType.MINUTES:
        minutes = interval_count
    td = timedelta(days=days, hours=hours, minutes=minutes)
    return(current_window[0] - td, current_window[1] - td)

def _check_input(interval_count):
    if not isinstance(interval_count, int):
        raise TypeError("interval_count must be an integer")

    if interval_count <= 0:
        raise ValueError("interval_count must be greater than zero")