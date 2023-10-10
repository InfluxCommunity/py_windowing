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
Currently the Windowing module supports months, days, hours, and minute time units, and works by defining the number of time units desired, and aligning the time window as described below. By defult, Windowing will use datetime.now() to calculate the current window, but users can provide their own "now" as well.

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
Windows will be aligned to the next larger supported unit. Specifically:
 * windows in minutes will be aligned to the 0th minute of the current hour
 * windows in hours will be aligned to the 0th hour of the current day
 * windows in days will be aligned to the 1st day of the current month
 * windows in months will be aligned to January 1 of the current year

For example, if you ask for a 1 minute window and the time is 12:15:15, the start of the window will be 12:15:00 of the current date, and the stop of the window will be 12:16:00 of the current date. This allows you to write queries for the window such as: ```WHEN time >= {start} and time < {stop} ```