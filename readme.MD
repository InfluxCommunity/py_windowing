# Windowing
This module is to assist with generating the start and stop time of time series queries in Python.

## The Problem
A typical time series query in InfluxQL or SQL to get all of the rows in a specific 10 minute window might look like this:

```sql
SELECT
    *
FROM
    my_table
WHERE
    WHERE time >= '2023-10-06T12:00:00Z' AND time < '2023-10-06T12:10:00Z'

```
For many types of analytic queries, the precision of the time windows is critical. For example, you want all of the rows from a specific hour, and you don't want any rows from a different hour. 

It's easy enough to set the time windows that you want when you are writing the queries interactively, but when your program is creating the queries on a schedule, it can require a lot of code to generate and align the desired time windows. This can be especially true if your program needs to calculate the previous or next window, which may fall over hour, day, month, or year boundaries.

## The Solution
The Windowing module simplifies the generation of time windows.

# Usage
Currently the Windowing module supports seconds, hours, and minute time units, and works by defining the number of time units desired, and aligning the time window as described below. By defult, Windowing will use datetime.now() to calculate the current window, but users can provide their own "now" as well.

The following example creates 10 minute intervals, and demonstrates retrieving the previous window, as well as getting the next 2 windows.

Import the library and create the window based on the current time
```python
>>> from windowing import Window, TimeUnit
>>> window = Window(time_unit=TimeUnit.MINUTES, unit_count=10)
```

Print out the start and stop time of the current window.
```python
>>> window.start, window.stop
(datetime.datetime(2023, 10, 6, 9, 20), datetime.datetime(2023, 10, 6, 9, 30))
```
Print out the previous window.
```python
>>> previous_window = window.previous_window
>>> print(previous_window.start, previous_window.stop)
2023-10-06 09:10:00 2023-10-06 09:20:00
```

Print out the next window.
```python
>>> next_window = window.next_window
>>> print(next_window.start, next_window.stop)
2023-10-06 09:30:00 2023-10-06 09:40:00
```

Print out even the next window.
```Python
>>> next_next_window = next_window.next_window
>>> print(next_next_window.start, next_next_window.stop)
2023-10-06 09:40:00 2023-10-06 09:50:00
```

Print out the next 10 windows.
```python
>>> for _ in range(10):
...     next_window = next_window.next_window
...     print(next_window.start, next_window.stop)
... 
2023-10-06 09:40:00 2023-10-06 09:50:00
2023-10-06 09:50:00 2023-10-06 10:00:00
2023-10-06 10:00:00 2023-10-06 10:10:00
2023-10-06 10:10:00 2023-10-06 10:20:00
2023-10-06 10:20:00 2023-10-06 10:30:00
2023-10-06 10:30:00 2023-10-06 10:40:00
2023-10-06 10:40:00 2023-10-06 10:50:00
2023-10-06 10:50:00 2023-10-06 11:00:00
2023-10-06 11:00:00 2023-10-06 11:10:00
2023-10-06 11:10:00 2023-10-06 11:20:00
```

The start and stop times for the windows are just Python datetime objects, so you can format them as needed in your code. For example, for InfluxQL.
```python
WHERE
    time >= '{window.start.strftime('%Y-%m-%d %H:%M:%S')}'
AND
    time < '{window.stop.strftime('%Y-%m-%d %H:%M:%S')}'
```

## Alignment
Currently, the module supports minutes, hours, and days and time units. 

### Minute Alignment
If you specific minutes as the time unit, the windows will align to the minute boundaries, starting at the bottom of the hour. Examples:
 * If your start time is 12:10, and you ask for 7 minute windows, the current window will be 12:07 to 12:14. The previous window will be 12:00 to 12:07, and the next window will be 12:21. 
 * If your start time is 12:10:30 (12:10 and 15 seconds), and you ask for 1 minute intervals, the seconds will be ignored, and your current window will be 12:10:00 to 12:11:00.

Note that the windows are not coerced to realign at the next hour if the length of the window is not a divsior of 60. So, in the above example with 7 minute windows, the window after 12:49 to 12:56 will be 13:03.

### Hour Alignment
Similar to minutes, if the chose time unit is in hours, the hours will align to 00:00 of the current day.

### Day Alignment
Day-based windows do not align to weeks or months, they simply start at the current day.

For example, if your start time is 2023-10-06 at 12:10, and you ask for 1 day windows, the current window will be 2023-10-06 00:00 to 2023-10-07 00:00.

# Why Not RRULE?
You may be familiar with the execllent [rrule library](https://dateutil.readthedocs.io/en/stable/rrule.html) and wonder why a windowing library was needed. 

Rrule is great for generating scheduled times off into the future, and if that is your need, you should definately consider it. However, rrule is more difficult to use if you want to calculate times in the past. Additionally, rrule requires a lot of manual code to align windows. Currently this module is not based on rrule, but it may be changed internally to use rrule under the hood in the future.