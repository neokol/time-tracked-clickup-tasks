import datetime

# helpers.py: This module includes function to convert date, hours etc


def unix_time(num1, num2, num3):
    """
    This function convert date to unix time stamp
    Parameters:
    num1,num2,num3 (int): Year, month, day

    Returns:
    (int): timestamp in unix
    """
    date_time = datetime.datetime(num1, num2, num3, 00, 00)
    unix_timestamp = datetime.datetime.timestamp(date_time)*1000
    return int(unix_timestamp)


def ms_to_hm(ms):
    """
    This function convert miliseconds to hours and minutes
    Parameters:
    ms: miliseconds of the task

    Returns:
    (int): hours and minutes
    """
    hours = 0
    minutes = 0
    hours = ms // 3600000
    ms %= 3600000
    minutes = ms // 60000
    return hours, minutes


def ms_to_hours(milis):
    milis = milis/3600000
    return milis


def time_entries_to_hours(time_entries):
    """
    This function receive a list of interval times of a task and sum it to one variable
    Parameters:
    (time_entries): Time entries of a task
    Returns:
    (int): total time of a task
    """
    # Counters set to zero
    total_time = 0
    total_hours = 0

    # Calculate time in total per task
    for y in range(len(time_entries)):
        total_time = total_time + time_entries[y]
        total_hours = total_hours + time_entries[y]

    return total_time, total_hours
