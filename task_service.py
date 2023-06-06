import io
import csv
from flask import session
import validators
import helpers
import api
import utils


def process_task_data(year, month, day, list_id):
    # Validate date
    is_valid, error_message = validators.validate_date(year, month, day)
    if not is_valid:
        return None, None, error_message

    # Converts the given year, month, and day into a Unix timestamp
    unix_timestamp = helpers.unix_time(year, month, day)

    # Call Function to Get all data from Click up api - Get All Tasks of a list
    data, error_message = api.get_clickup_data(unix_timestamp, list_id)

    # Check if there is an error with the request
    if error_message:
        return None, None, error_message
    # Get all lists needed

    tasks_id, tasks_name, tasks_status, date_created, date_closed = utils.get_non_custom_clickup_fields(
        data)
    # Get custom field Invoice Description
    tasks_invoice_descr = utils.get_invoice_description(data)

    # Get all Time of all Tasks
    # time_tracked contains hours as numbers and time logged contains time as hours and minutes
    time_tracked, time_logged = utils.get_time_entries_per_task(
        tasks_id, unix_timestamp)

    # Give headers of Table
    header = ['ID', 'Name', 'Invoice Description', 'Status',
              'Date Created', 'Date Closed', 'Time Logged', 'Time in hours']

    # combining these lists into one list of tuples
    data_rows = list(zip(tasks_id, tasks_name, tasks_invoice_descr,
                         tasks_status, date_created, date_closed, time_tracked, time_logged))

    return data_rows, header, None


# In task_service.py
