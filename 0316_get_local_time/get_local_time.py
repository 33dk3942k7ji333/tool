import datetime
import time

def get_local_datetime_string():
    """
    Returns the current local date and time as a formatted string.
    """
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def get_local_date_string():
    """
    Returns the current local date as a formatted string.
    """
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")

def get_local_time_string():
    """
    Returns the current local time as a formatted string.
    """
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S")

def get_local_datetime_with_offset():
    """
    Returns the current local date and time, and timezone offset, as a formatted string.
    """
    now = datetime.datetime.now()
    offset_seconds = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    offset_hours = offset_seconds / -3600.0
    offset_str = "{:+03.0f}:{:02.0f}".format(offset_hours, abs(offset_hours * 60) % 60)
    return now.strftime("%Y-%m-%d %H:%M:%S") + " UTC" + offset_str

# Example usage:
datetime_string = get_local_datetime_string()
date_string = get_local_date_string()
time_string = get_local_time_string()
datetime_offset_string = get_local_datetime_with_offset()

print(f"Current date and time: {datetime_string}")
print(f"Current date: {date_string}")
print(f"Current time: {time_string}")
print(f"Current date and time with offset: {datetime_offset_string}")