from datetime import datetime, timedelta
from enum import Enum
from dateutil.relativedelta import relativedelta

class TimeUnit(Enum):
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"
    MONTHS = "months"

class Window():
    def __init__(self, unit_count=1, time_unit=None, now=None):
        _check_unit_count(unit_count)
        if time_unit is None:
            raise ValueError("unit_type must not be None")
        if now is None:
            now = datetime.now()

        self.unit_count = unit_count
        self.time_unit = time_unit
        self.start, self.stop = get_current_window(unit_count, time_unit, now)
    
    @property
    def next_window(self):
        return Window(self.unit_count, self.time_unit, self.stop)
    
    @property
    def previous_window(self):
        start, stop = get_previous_window(self.unit_count, self.time_unit, self.start)
        return Window(self.unit_count, self.time_unit, start)

def get_next_window(unit_count, unit_type, now=None):
    _check_unit_count(unit_count)
    current_window = get_current_window(unit_count, unit_type, now)
    days, hours, minutes, months = 0, 0, 0, 0

    if unit_type == TimeUnit.DAYS:
        days = unit_count
    elif unit_type == TimeUnit.HOURS:
        hours = unit_count
    if unit_type == TimeUnit.MINUTES:
        minutes = unit_count
    if unit_type == TimeUnit.MONTHS:
        months = unit_count
    # td = timedelta(months=months, days=days, hours=hours, minutes=minutes)
    td = relativedelta(months=months, days=days,hours=hours,minutes=minutes)
    return(current_window[0] + td, current_window[1] + td)
    
def get_current_window(unit_count, unit_type, now=None):
    _check_unit_count(unit_count)
    
    if now == None:
        now = datetime.now()

    if unit_type == TimeUnit.MINUTES:
            hours = unit_count // 60
            start = now
            if unit_count < 60:
                minute = (now.minute // unit_count) * unit_count
                if minute >= 60:
                    start = now.replace(minute=0, second=0, microsecond=0)
                else:
                    start = now.replace(minute=minute, second=0, microsecond=0)
            else:
                start = now.replace(minute=0, second=0, microsecond=0)
            stop_time = start + timedelta(minutes=unit_count)
            stop = stop_time.replace(second=0, microsecond=0)
            return (start, stop)
    
    if unit_type == TimeUnit.HOURS:
        start = now.replace(hour=now.hour, minute=0, second=0, microsecond=0)

        days = unit_count // 24
        
        stop_time = now + timedelta(days = days, hours=unit_count)
        stop = stop_time.replace(minute=0, second=0, microsecond=0)
        return (start, stop)
        
    if unit_type == TimeUnit.DAYS:
        start = now.replace(day=now.day, hour=0, minute=0, second=0, microsecond=0)
        
        stop_time = now + timedelta(days = unit_count)
        stop = stop_time.replace(hour=0, minute=0, second=0, microsecond=0)
        return (start, stop)
    
    if unit_type == TimeUnit.MONTHS:
        
        start_month = ((now.month - 1) // unit_count) * unit_count + 1
        start = now.replace(month=start_month, day=1, hour=0, minute=0, second=0,microsecond=0)
        stop = start  + relativedelta(months=unit_count)

        return start, stop

def get_previous_window(unit_count, unit_type, now=None):
    _check_unit_count(unit_count)
    current_window = get_current_window(unit_count, unit_type, now)
    days, hours, minutes = 0, 0, 0

    if unit_type == TimeUnit.MONTHS:
        return(current_window[0] - relativedelta(months=unit_count), current_window[0])

    if unit_type == TimeUnit.DAYS:
        days = unit_count
    elif unit_type == TimeUnit.HOURS:
        hours = unit_count
    if unit_type == TimeUnit.MINUTES:
        minutes = unit_count
    td = timedelta(days=days, hours=hours, minutes=minutes)
    return(current_window[0] - td, current_window[1] - td)

def _check_unit_count(unit_count):
    if not isinstance(unit_count, int):
        raise TypeError("interval_count must be an integer")

    if unit_count <= 0:
        raise ValueError("interval_count must be greater than zero")