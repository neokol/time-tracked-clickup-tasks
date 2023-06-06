import calendar

# validators.py:This module includes validation for the form

# Function to validate the provided date


def validate_date(year, month, day):
    """
    This function validates the data from the form
    Parameters:
    year,month, day (int): The dates we want to use as parameters to request

    Returns:
    (bool): True if the data is valid, False if the data is invalid
    (error message): Error message to describe the issue
    """
    try:
        year = int(year)
        month = int(month)
        day = int(day)
    except ValueError:
        return False, "Year, month, and day must be integers."
    # Check if the year is within the allowed range
    if not (2000 <= year <= 2999):
        return False, "Enter a valid year"
    # Check if the day is possible for the given year and month
    if not (1 <= month <= 12):
        return False, "Month must be between 1 and 12"
    # check if day is not out of range before validating with the specific month
    if not (1 <= day <= 31):
        return False, "Day must be between 1 and 31"
    # If all checks passed, the date is valid
    _, num_days_in_month = calendar.monthrange(year, month)
    if day > num_days_in_month:
        return False, f"Day must be between 1 and {num_days_in_month} for the selected month and year."

    return True, None
