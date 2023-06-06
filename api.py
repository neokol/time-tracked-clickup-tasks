import requests
import helpers
import config
import time

# api.py: This module includes all API calls to ClickUp and their corresponding data processing functions.


def get_clickup_data(unix_timestamp, list_id):
    """
    This function retrieves all task's list from ClickUp API  
    Parameters:
    unix_timestamp (int): The date of the tasks we want to retrieve in Unix timestamp format.
    list_id (str): The ID of the list we want to retrieve tasks from.

    Returns:
    tuple: a tuple containing the retrieved data and an error message if any.
    """

    # Request to get all tasks from the selected list
    url = "https://api.clickup.com/api/v2/list/" + list_id + "/task"

    query = {
        "include_closed": "true",
        "subtasks": "true",
        "date_updated_gt": f"{(unix_timestamp)}"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{config.api_token}"
    }

    response = requests.get(url, headers=headers, params=query)
    # Save the data
    data = response.json()

    # Check if connection status is OK
    if response.status_code == 200:
        return data, None
    elif response.status_code == 404:
        return None, "List not found"
    else:
        return None, "An error occurred"

# Time logged is in another request
# Use a for loop to search every task from the Task id list


def get_time_tracked_per_task(task_id):
    """
    This function retrieves all time tracked from a task of ClickUp API  
    Parameters:
    task_id: The ID of the task we want to retrieve data from.

    Returns:
    tuple: a tuple containing the retrieved data
    """

    # Make time Tracked Requests to Get time per task
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{config.api_token}"
    }

    url_time_tracked = "https://api.clickup.com/api/v2/task/" + \
        str(task_id + "/time")
    response_time_tracked = requests.get(
        url_time_tracked, headers=headers)
    time_per_task = response_time_tracked.json()

    return time_per_task
