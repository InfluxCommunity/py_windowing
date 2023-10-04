from datetime import datetime, timedelta
from enum import Enum

class IntervalType(Enum):
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"
    SECONDS = "seconds"

def get_next_window(interval_count, interval_type, now=None):
    if interval_type == IntervalType.MINUTES:
        t =  _get_next_start_minutes(interval_count, now)
        return (t, t + timedelta(minutes=interval_count))
    elif interval_type == IntervalType.HOURS:
        t = _get_next_start_hours(interval_count, now)
        return (t, t + timedelta(hours=interval_count))
    elif interval_type == IntervalType.DAYS:
        t = _get_next_start_days(interval_count, now)
        return (t, t + timedelta(days=interval_count))
    
def get_current_window(interval_count, interval_type, now=None):
    if now == None:
        now = datetime.now()

    if interval_type == IntervalType.MINUTES:
        start = now.replace(second=0, microsecond=0)

        hours = interval_count // 60
        stop_time = now + timedelta(hours = hours, minutes=interval_count)
        stop = stop_time.replace(second=0, microsecond=0)
        return (start, stop)
    
    if interval_type == IntervalType.HOURS:
        start = now.replace(hour=now.hour, minute=0, second=0, microsecond=0)

        days = interval_count // 24
        
        stop_time = now + timedelta(days = days, hours=interval_count)
        stop = stop_time.replace(minute=0, second=0, microsecond=0)
        return (start, stop)
        


def _get_next_start_minutes(minutes, now=None):
    if now == None:
        now = datetime.now()

    if minutes < 60:
        next_minute = ((now.minute // minutes) + 1) * minutes
        if next_minute >= 60:
            return now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        else:
            return now.replace(minute=next_minute, second=0, microsecond=0)
    else:
        return now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

def _get_next_start_hours(hours, now=None):
    if now == None:
        now = datetime.now()
    return now.replace(hour=now.hour + 1, minute=0, second=0, microsecond=0)

def _get_next_start_days(days, now=None):
    if now == None:
        now = datetime.now()
    return now.replace(day = now.day + 1, hour=0, minute=0, second=0, microsecond=0)
   

def get_then(interval_val, interval_type, now):
    if interval_type == "m":
        return now - timedelta(minutes=interval_val)
    elif interval_type == "h":
        return now - timedelta(hours=interval_val)
    elif interval_type == "d":
        return now - timedelta(days=interval_val)