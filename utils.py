import helpers
import time
import api

# utils.py: This module includes the data proceesing


def get_non_custom_clickup_fields(data):
    """
    This function receives the Tasks and provides the lists of the requested fields

    Parameters:
    data: Response from the API Tasks

    Returns:
    (tuples): fields required
    """
    tasks_id = [str(task['id']) for task in data['tasks']]
    # Save all Task Name
    tasks_name = [str(task['name']) for task in data['tasks']]
    # Save all Task Status
    tasks_status = [str(task['status']['status'])
                    for task in data['tasks']]
    # Save Date Created
    date_created = [
        time.strftime(
            '%Y-%m-%d', time.gmtime(int(task['date_created'])/1000))
        for task in data['tasks']
    ]
    # Save Date Closed
    date_closed = [
        time.strftime(
            '%Y-%m-%d', time.gmtime(int(task['date_closed'])/1000))
        if task['date_closed'] is not None else 'null' for task in data['tasks']
    ]
    return tasks_id, tasks_name, tasks_status, date_created, date_closed


# Get custom field Invoice Description
def get_invoice_description(data):
    """
    This function receives the Tasks and provides a list of custom field Invoice Descripition of existed
    Parameters:
    (data): Response from the API Tasks

    Returns:
    (tuple): List of Invoice Description
    """

    # Save Invoice Description - In custom fields list
    tasks_invoice_descr = []
    for i in range(len(data['tasks'])):
        for j in range(len(data['tasks'][i]['custom_fields'])):
            # Search for the name of the task
            if (data['tasks'][i]['custom_fields'][j]['name']) == 'Invoice Description':
                # Check the task have the value
                if 'value' in data['tasks'][i]['custom_fields'][j]:
                    tasks_invoice_descr.append(
                        str(data['tasks'][i]['custom_fields'][j]['value']))
                else:
                    tasks_invoice_descr.append('Null')

    return tasks_invoice_descr


def get_time_entries_per_task(tasks_id, unix_timestamp):
    """
    This function receives a list of tasks ids and a timestamp and provides a two lists of time of every given task
    Parameters:
    tasks_id: List of with ids
    unix_timestamp: the date from 

    Returns:
    (tuple): Two lists of time of every given task
    """

    # List to save all time tracked per task
    time_tracked = []
    # Temporary list to save time entries
    time_entries = []
    # List to transform time from tasks to hours and minutes
    time_logged = []
    for j in range(len(tasks_id)):
        time_per_task = api.get_time_tracked_per_task(tasks_id[j])
        user_time_logged = 0
        if len(time_per_task['data']) != 0:
            # For-loop inside the entries of the request per user
            for x in range(len(time_per_task['data'])):
                # For-loop inside the intervals to get all entries per user
                for y in range(len(time_per_task['data'][x]['intervals'])):
                    if int(time_per_task['data'][x]['intervals'][y]['end']) >= unix_timestamp:
                        # Sum of hours of all users
                        user_time_logged = user_time_logged + \
                            (int(time_per_task['data'][x]
                             ['intervals'][y]['time']))

                    else:
                        user_time_logged = user_time_logged + 0
            # Add the sum hours to the list and zero the sum for the next task
            time_entries.append(int(user_time_logged))
            user_time_logged = 0
        else:
            time_entries.append(0)

        # Call function to get the total time of a task
        total_time, total_hours = helpers.time_entries_to_hours(time_entries)

        # Add the total time to the list - After converted to hours
        time_tracked.append(str(helpers.ms_to_hours(total_time)))

        time_logged.append(
            f'{helpers.ms_to_hm(total_hours)[0]}h {helpers.ms_to_hm(total_hours)[1]}m')
        # Clear the list for the next task
        time_entries.clear()

    return time_tracked, time_logged
