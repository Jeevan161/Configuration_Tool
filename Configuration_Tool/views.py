import json
import time

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render


# Create your views here.
def home_view(request):
    return render(request, 'Base/Home.html')


def start_session_and_login():
    """Initialize session and log in to the system."""
    session = requests.Session()
    login_url = "https://nkb-backend-ccbp-beta.earlywave.in/admin/login/"
    username = 'content_loader'
    password = 'content_loader@432'

    # Log in to the system
    csrf_token = get_csrf_token(session, login_url)
    login_data = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token
    }
    headers = {
        'Referer': login_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
    }

    # Perform login
    session.post(login_url, data=login_data, headers=headers)
    return session


# Function to get CSRF token
def get_csrf_token(session, url):
    """Retrieve and return the CSRF token from the specified URL."""
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    return csrf_token


def get_task_details(request, request_id, check_interval=10):
    """Fetch task details based on the request ID and keep checking until status is 'SUCCESS' or 'FAILED'."""
    session = start_session_and_login()  # Reuse the session
    url = f"https://nkb-backend-ccbp-beta.earlywave.in/admin/nkb_load_data/contentloading/{request_id}/change/"

    task_output_url = None
    task_status = None

    while True:
        response = session.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract Task Output URL
            task_output_div = soup.find('div', class_='form-row field-task_output_url')
            task_output_url = task_output_div.find('div',
                                                   class_='readonly').text.strip() if task_output_div else "No Task Output URL found"

            # Extract Task Status
            task_status_div = soup.find('div', class_='form-row field-task_status')
            task_status = task_status_div.find('div',
                                               class_='readonly').text.strip() if task_status_div else "No Task Status found"

            # Print the task status for debugging
            print(f"Task Status: {task_status}")

            # Keep polling only if the task is still IN_PROGRESS
            if task_status not in ["IN_PROGRESS"]:
                print(f"Breaking the loop as task status is: {task_status}")
                break

        # Wait before checking again
        print(f"Waiting {check_interval} seconds before checking again...")
        time.sleep(check_interval)

    # Extract additional data based on the final task status
    output_link = "No Output Available"
    exception_message = "No Exception"

    if task_status in ["SUCCESS", "FAILED"]:
        try:
            # Directly parse the task_output_url as JSON string
            task_output_data = json.loads(task_output_url)

            # Extract URLs from JSON
            output_link = task_output_data.get("output", "No Output URL Found")
            exception_url = task_output_data.get("exception", None)

            # Set exception message to link if an exception exists
            if exception_url:
                exception_message = f'<a href="{exception_url}" target="_blank">View Exception Details</a>'
            else:
                exception_message = "No Exception"

        except json.JSONDecodeError:
            # Handle case where task_output_url was not a valid JSON
            exception_message = "Error parsing task output."

    # Pass data to the template
    context = {
        "task_status": task_status,
        "output_link": output_link,
        "exception_message": exception_message,
    }
    return render(request, 'Base_templates/Task_details.html', context)
