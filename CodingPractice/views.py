from django.shortcuts import render

# Create your views here.
import zipfile
import os
import shutil

import boto3
import gspread
import uuid
import requests
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
import re
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse

AWS_ACCESS_KEY_ID = 'ASIARTUZIEISKAOEK6LA'
AWS_SECRET_ACCESS_KEY = 'RrTs5FXUZl5xsPvr0PcvoE/PedthmPC+11NzS78W'
AWS_SESSION_TOKEN = 'IQoJb3JpZ2luX2VjEAQaCmFwLXNvdXRoLTEiRzBFAiEA95gEdDby6bqG/u/lQtrGYMHBFqkegOhwwKqyqauvAy8CICYkrkSSw5bI+S0eIM/QGWVQo8se33EbLcmAIE4mRn2aKr4ECG0QAxoMMTEwOTE2ODA1MTU2IgwrIlQkm9dmpakCKmEqmwSYLoqp1JMi8WICoN/n/h6PRM2/X6eldFT5fUWXyZr5RMLNj1INa8RGUeoLBjznz1qNZzC0q/APc24KZZDwf+y9kwUCLrJze7q9BZRJzihRCNu/X1Z4xhYtMdKjxHo/QVES2jYBeIvcoo7uA+vWZF6/5iVaXcokqeh7Jt+H6G16Gu+6beNphem7Ddn8i0bZK/pE/A/JwA8UySw4YwlrFsYJqMGS/i6vxHumUXaarXZsVQ9ivTi2tV1uJIcutg5ReIgJcv8PvCW+gnnHXz0tu+mV3P2q443Ev4o4N3OR7VpGQLyxgyprhFuMWkW3hFg9dnOZcLWyC3qNY+m9lvqE+lCyEdjtqOyg7qD2zcNpk21W0nvqeu6Pa4QnB2sgc3kzMzTTquQlmhqTY3Utu+xqkPQzoQvbIYLeyDpiwqguNkky2V6fPdHkk2U9MPgYcvKzaa1yZ0LOtBsXAvHG8ZLcsC8DCmMqJMBTaGry/td9wZStZZVmqA7l6E7i8Wc5YYsi8kvrBMRauIZ829Lzb9tNa5otgQK4fhJ2iNxT4+9ncoktwUoOpEwy4hhPNxKMxxLuuo8i7ELm8/D00DtfvEBeIjU0c3/uUyDqJP2MeG8gXJS9skPKQ7BegorlMhy1Vh36H5klkACvd8BTtfBrrJSplaC5j01PjvMLiv6zUe3HvIhWSeX6cCIpQxmwXkTx+z3N5oZASUvQD6JwcvzLIDCK+dG4BjqFAn2+CU5ygA8DRDiqS13lA+PPKb5NGSETaaXb5aZifpEf6C594DHwhDJ55u4nIay9HXc2tlq6JbqzhEksI21EqpsGYUsfWJv2yprM7BDLdFIvSBRNvhMuobd8oIOUyBRfVKLUSaLh9YR01ExoTbH4+ZchCHnikqPZLyKh0enI/szVON5L4akcu2nOEtb/TQu6p0rHFQ+DN3sPo5Ioq/5DgcA/In/3z21LYIulMQEFyBK/c7zAQnEcrhh3TaTzjSXj255Kt1Z2sXCVK+SX8WRNGctfxgQiiePDXPIad75xcaKKQeqrzsBnAhbxswpXYhTiLJ3KGjckE5PJWXQCBG6SOR+kAQxV2g=='  # Optional, if using temporary credentials
S3_BUCKET_NAME = 'nkb-backend-ccbp-media-static'
S3_REGION_NAME = 'ap-south-1'
S3_UPLOAD_FOLDER = 'ccbp_beta/media/content_loading/uploads/'


# Define the service account credentials directly
GOOGLE_SHEET_CREDENTIALS = {
    "type": "service_account",
    "project_id": "corded-pivot-429113-g1",
    "private_key_id": "4e9d7f0ed8b4ee6e34c5035a30c63eb7c0362f4c",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDR75dROrzRJ2Tc\n0jA6vBwyHqP1AZwLQ5lmViWbNzPmSknePYCjSxAPLOlogwXOgkiR/TuNUVUe+T7a\n9A5dEcYi/dACZZ406lYM22i0+2Q9oyDYXqTzjdtLI3cGLMXRE1CwKSKIstg6YbZq\n/IKiKsuw5kgcpS8y/Y3kqHC/Fmt9ycf6MDytDc2KUXZHYFI3rURo64P9MoNq2CyJ\nkmnHGc88wohTd6IEZ98MzBHe6wgslnkqQQdtiyn8jfHmKhxBwJG3ahQ5KdSR9H+J\ng7mlak/D3L2a0pzul/g2iDOh9EvbZ5OF/dZRR5htUgqiGykBA4DHBss87BxmrQIJ\n3lVAkKxPAgMBAAECggEAaMQh5gojh1ca+S41nmIYyhRLay4R8vcZux3bp5GNZ2wE\nYBGePB9uFLyrgJn+UFfpIl3XFceUbKAi836fGmgP0o+Kel++65ZUOhdWshbQqAfc\nEM5ukBLncKByuhSm5Zc3iaoFj2V9DemMcOixwn8L5qyNKSpwGwi5AnbiySHFo+Ai\nT2VM6dvWQBCzNR91gBAQNkbxFqu+kygAHetVdf0ClOOi52WoiAnDHjXbn9Ollco7\nv1l21CAtY/OJoHR1PhNjEq5L019kuO+KPdGAJ3AMxlNGhKvXE48nDgifjalCsgZM\nI+HiyykdfHxRec1FsB0FEzxbGAiF58pMO7XoLLpsrQKBgQD58kksMluBw97aBpxn\nHhdDk9V83bQbOAc4f8K4OTU+pZII2VykidZKH2is8JGJXvKyD8JlV2CwLGlfsELv\n+S7neNcVg6tU4gE6CJniFMl7q1UGDecWRY3/ZqW+7F+xXPH+leWMY5cstqGHcdIf\nt41yxsSjgml0pwcKkcRSJ85MYwKBgQDXBTuKG8RxawYRtXiSEBE6c4oXEA0zbj/S\noKhyoYY1YNqH6iiUQcxGRgm6esCCR3af+znxMJxgZXmhlm0iTKBjIrenmJ72WTtn\nXrurEwcXmr4ydwsgmGdkMvJ4WsqlKxnk1r/cZh1non8LHGnWUs4zqiM9+Zg5ZyRY\nIUhW8m52JQKBgFjglrRok7Fo/O16PFNOl+cnwlpMW6byHV8xzwPDE/Pa3DrZT+AS\nQ2jIEmisgpPed15pzC5NC8yZfj7QZnz+lncouRKlZ18fnmAMfuutiJe5LNqiRvHc\necm/rmBdnQlsi4CDvMRXBYKYzodjKdytYFbX50RdMzKP0ikn/C9aiDkRAoGBAM/L\nv8F1mj/dpQziKnZFztCFLjOhkJBegJFmL8QwM0pMooRtF/BHMknLj8VGsdp1g7+S\nA2oCh21lQ8mUXT2jffCwcXonNaBvlcgNNiJbDiSSqDKO9xL2Fh0wW0FSxLogUDLm\nEp7FlK89y7cKK4IznhEx4EMZfjIjam09JPLZ8UR9AoGAVSHXdf2ieG7xc1XYxBl1\n8voXu8+5QdoOAZeboEC7tzK+iuUoFCX6zlyGV9YrT0tcbbB1a4RQixcXROe1uQJ/\n2aSvpcKjLuzEmGQ86q+cAtXQjGmx8LieUAWI23dLds42nnEkUwKh9/8mKoYdxp+p\nc3OJ/lkd1vnzMVBAmA9lkn8=\n-----END PRIVATE KEY-----\n",
    "client_email": "tutorial-configuration-script@corded-pivot-429113-g1.iam.gserviceaccount.com",
    "client_id": "111171826741023448042",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/tutorial-configuration-script%40corded-pivot-429113-g1.iam.gserviceaccount.com",
}
def extract_aws_credentials(session):
    """
    Extract AWS credentials from the HTML response.
    """
    url = "https://nkb-backend-ccbp-beta.earlywave.in/admin/nkb_load_data/uploadfile/add/"
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the script tag containing the credentials
    script_tag = soup.find("script", text=re.compile("AWS.Credentials"))
    if not script_tag:
        print("Could not find AWS credentials script.")
        return None

    # Extract credentials using regular expressions
    aws_access_key_id = re.search(r"AWS\.Credentials\(\s*'([^']+)'", script_tag.text)
    aws_secret_access_key = re.search(r"AWS\.Credentials\(\s*'[^']+',\s*'([^']+)'", script_tag.text)
    aws_session_token = re.search(r"AWS\.Credentials\(\s*'[^']+',\s*'[^']+',\s*'([^']+)'", script_tag.text)

    if aws_access_key_id and aws_secret_access_key and aws_session_token:
        credentials = {
            "aws_access_key_id": aws_access_key_id.group(1),
            "aws_secret_access_key": aws_secret_access_key.group(1),
            "aws_session_token": aws_session_token.group(1)
        }
        print(f"Extracted AWS Credentials: {credentials}")
        return credentials
    else:
        print("Failed to extract AWS credentials.")
        return None


def set_aws_credentials():
    """Set AWS credentials by logging in and extracting them from the HTML page."""
    session = start_session_and_login()
    if session:
        credentials = extract_aws_credentials(session)
        if credentials:
            global AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN
            AWS_ACCESS_KEY_ID = credentials['aws_access_key_id']
            AWS_SECRET_ACCESS_KEY = credentials['aws_secret_access_key']
            AWS_SESSION_TOKEN = credentials['aws_session_token']
        else:
            print("Failed to obtain AWS credentials from the HTML response.")


def submit_sheet_loading_request(final_json):
    """Send a request to initiate sheet loading using the prepared final JSON."""
    session = start_session_and_login()
    form_url = "https://nkb-backend-ccbp-beta.earlywave.in/admin/nkb_load_data/contentloading/add/"
    csrf_token = get_csrf_token(session, form_url)

    # Prepare the form data
    input_data = json.dumps(final_json)
    form_data = {
        "csrfmiddlewaretoken": csrf_token,
        "task_type": "SHEET_LOADING",
        "input_data": input_data,
        "_continue": "Save and view"
    }

    # Set headers and send POST request
    headers = {
        'Referer': form_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
    }

    response = session.post(form_url, data=form_data, headers=headers, allow_redirects=True)

    # Log the response for debugging
    if response.history:
        final_referer_url = response.url
        match = re.search(r'/contentloading/([a-f0-9\-]+)/change/', final_referer_url)
        if match:
            requested_id = match.group(1)
            print(f"Extracted Requested ID: {requested_id}")
            # Redirect to task details page with `requested_id` in URL
            return redirect('task_details', request_id=requested_id)

    if response.status_code == 200:
        print("Sheet loading request was successful.")
    else:
        print(f"Failed to load the sheet: {response.status_code} - {response.text[:500]}")

    return response


def start_session_and_login():
    """Start a session and login to the system."""
    session = requests.Session()
    login_url = "https://nkb-backend-ccbp-beta.earlywave.in/admin/login/"

    # Get CSRF token
    login_page = session.get(login_url)
    soup = BeautifulSoup(login_page.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

    # Login credentials and token
    login_data = {
        'username': 'content_loader',
        'password': 'content_loader@432',
        'csrfmiddlewaretoken': csrf_token
    }

    headers = {
        'Referer': login_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.89 Safari/537.36'
    }

    # Log in to the session
    response = session.post(login_url, data=login_data, headers=headers)

    if "Log out" in response.text or response.url != login_url:
        print("Login successful.")
    else:
        print("Login failed.")
        print("Response Text:", response.text[:500])  # Print part of the response for debugging

    return session


def get_csrf_token(session, url):
    """Get the CSRF token from a given URL."""
    page = session.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    return csrf_token

def upload_to_s3(file_path):
    """Upload a file to AWS S3 and return the file URL."""
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN,  # Omit this if not using temporary credentials
        region_name=S3_REGION_NAME
    )

    # Generate a unique file name using UUID
    file_name = os.path.basename(file_path)
    unique_file_name = f"{uuid.uuid4()}_{file_name}"
    s3_key = f"{S3_UPLOAD_FOLDER}{unique_file_name}"

    try:
        print(f"Attempting to upload file {file_path} to S3 bucket {S3_BUCKET_NAME} at {s3_key}")
        s3_client.upload_file(file_path, S3_BUCKET_NAME, s3_key, ExtraArgs={'ACL': 'public-read'})
        s3_file_url = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION_NAME}.amazonaws.com/{s3_key}"
        print(f"File uploaded successfully to: {s3_file_url}")
        return s3_file_url
    except Exception as e:
        print(f"Failed to upload to S3: {e}")
        return None


def prepare_json(resource_id, title, duration, parent_id, child_order):
    """
    Prepare JSON data based on the user inputs.
    """
    common_unit_id = str(uuid.uuid4())

    # Create JSON based on the example format
    json_data = {
        "ResourcesData": [
            {
                "resource_id": resource_id,
                "resource_type": "UNIT",
                "dependent_resource_count": 0,
                "parent_resource_count": 1,
                "auto_unlock": True
            },
            {
                "child_order": child_order,
                "parent_resources": parent_id
            }
        ],
        "Units": [
            {
                "unit_id": resource_id,
                "common_unit_id": common_unit_id,
                "unit_type": "QUESTION_SET",
                "duration_in_sec": duration,
                "tags": "MOCK_TEST_EVALUATION"
            }
        ],
        "QuestionSet": [
            {
                "question_set_id": resource_id,
                "title": title,
                "content_type": "CODING"
            }
        ]
    }

    # Print JSON for debugging
    print(json.dumps(json_data, indent=4))

    return json_data


def rename_json_files_in_zip(zip_file, output_dir):
    """
    Rename all JSON files in the provided ZIP with a new UUID without changing the structure.
    Returns the new UUID used for renaming and the path of the modified ZIP.
    """
    temp_extract_dir = os.path.join(output_dir, 'temp_extract')
    temp_output_dir = os.path.join(output_dir, 'temp_output')

    # Create temp directories for extraction and output
    os.makedirs(temp_extract_dir, exist_ok=True)
    os.makedirs(temp_output_dir, exist_ok=True)

    # Extract the uploaded zip file
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(temp_extract_dir)

    # Generate a new UUID for renaming JSON files
    new_uuid = str(uuid.uuid4())

    # Walk through the extracted files, retain structure, and rename JSON files
    for dirpath, dirnames, filenames in os.walk(temp_extract_dir):
        for filename in filenames:
            src_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(src_path, temp_extract_dir)
            dest_path = os.path.join(temp_output_dir, relative_path)

            # Create directories in the output directory (preserving folder structure)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            # If it's a JSON file, rename it to {new_uuid}.json
            if filename.endswith('.json'):
                new_filename = f"{new_uuid}.json"
                dest_path = os.path.join(os.path.dirname(dest_path), new_filename)

            # Copy the file (renaming JSON files, preserving others)
            shutil.copy(src_path, dest_path)

    # Create the final zip file with renamed JSONs and the original structure
    final_zip_path = os.path.join(output_dir, f"modified_{new_uuid}.zip")
    with zipfile.ZipFile(final_zip_path, 'w') as new_zip:
        for dirpath, dirnames, filenames in os.walk(temp_output_dir):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                arcname = os.path.relpath(file_path, temp_output_dir)  # Retain folder structure in zip
                new_zip.write(file_path, arcname)

    # Cleanup temp directories
    shutil.rmtree(temp_extract_dir)
    shutil.rmtree(temp_output_dir)

    return new_uuid, final_zip_path



def upload_to_google_sheets(json_data, sheet_name):
    """
    Uploads the processed JSON data to Google Sheets.
    """
    # Step 1: Authenticate and create a client to interact with Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_SHEET_CREDENTIALS, scope)
    client = gspread.authorize(creds)

    # Step 2: Create a new Google Spreadsheet with the provided name
    spreadsheet = client.create(sheet_name)

    # Step 3: Share the spreadsheet with editor access
    spreadsheet.share('learningresource@nkblearningbackend.iam.gserviceaccount.com', perm_type='user', role='writer')
    spreadsheet.share('jeevansravanth.parisa@nxtwave.co.in', perm_type='user', role='writer')

    # Step 4: Create Sheets for each JSON section and add data
    # Sheet 1: ResourcesData
    resources_data_sheet = spreadsheet.add_worksheet(title="ResourcesData", rows="100", cols="20")
    resources_data_sheet.append_row([
        "resource_id", "resource_type", "dependent_resource_count", "dependent_resources",
        "dependent_reason_display_text", "parent_resource_count", "child_order",
        "parent_resources", "auto_unlock"
    ])

    for resource in json_data.get("ResourcesData", []):
        # Append parent resource row data
        resources_data_sheet.append_row([
            resource.get("resource_id"),
            resource.get("resource_type"),
            resource.get("dependent_resource_count"),
            resource.get("dependent_resources"),
            resource.get("dependent_reason_display_text"),
            resource.get("parent_resource_count"),
            "",  # Empty because this row represents the parent
            "",  # Empty because this row represents the parent
            resource.get("auto_unlock", "")
        ])

        # Append child data for the resource
        resources_data_sheet.append_row([
            "", "", "", "", "", "",  # Empty columns for parent-specific fields
            resource.get("child_order", ""),
            resource.get("parent_resources", ""),
            ""  # Empty because this field doesn't apply to the child
        ])

    # Sheet 2: Units
    units_sheet = spreadsheet.add_worksheet(title="Units", rows="100", cols="20")
    units_sheet.append_row(["unit_id", "common_unit_id", "unit_type", "duration_in_sec", "tags"])
    for unit in json_data.get("Units", []):
        units_sheet.append_row([
            unit.get("unit_id"),
            unit.get("common_unit_id"),
            unit.get("unit_type"),
            unit.get("duration_in_sec"),
            unit.get("tags")
        ])

    # Sheet 3: QuestionSet
    question_set_sheet = spreadsheet.add_worksheet(title="QuestionSet", rows="100", cols="20")
    question_set_sheet.append_row(["question_set_id", "title", "content_type"])
    for question_set in json_data.get("QuestionSet", []):
        question_set_sheet.append_row([
            question_set.get("question_set_id"),
            question_set.get("title"),
            question_set.get("content_type")
        ])

    # Provide the link to the spreadsheet
    return {
        "message": f"Spreadsheet '{sheet_name}' created successfully.",
        "url": spreadsheet.url  # URL of the created spreadsheet
    }


def submit_unlock_request(resource_id):
    """Send a request to unlock resources for users using the provided resource ID."""
    session = start_session_and_login()
    form_url = "https://nkb-backend-ccbp-beta.earlywave.in/admin/nkb_load_data/contentloading/add/"
    csrf_token = get_csrf_token(session, form_url)

    # Prepare the form data
    input_data = json.dumps({
        "resource_ids": [resource_id]
    })

    form_data = {
        "csrfmiddlewaretoken": csrf_token,
        "task_type": "UNLOCK_RESOURCES_FOR_USERS",
        "input_data": input_data,
        "_continue": "Save and view"
    }

    # Set headers and send POST request
    headers = {
        'Referer': form_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
    }

    response = session.post(form_url, data=form_data, headers=headers, allow_redirects=True)

    # Extract the requested ID from the redirect URL
    if response.history:
        final_referer_url = response.url
        match = re.search(r'/contentloading/([a-f0-9\-]+)/change/', final_referer_url)
        if match:
            requested_id = match.group(1)
            print(f"Unlock request completed. Extracted Requested ID: {requested_id}")
            return redirect('task_details', request_id=requested_id)

    return HttpResponse("Failed to submit unlock request.")


def upload_and_prepare(request):
    if request.method == 'POST':
        zip_file = request.FILES['zip_file']
        title = request.POST['title']
        parent_id = request.POST['parent_id']
        child_order = int(request.POST['child_order'])
        duration = int(request.POST['duration'])

        # Step 1: Rename JSON files in the zip
        output_dir = "media/output"
        resource_id, modified_zip_path = rename_json_files_in_zip(zip_file, output_dir)

        # Step 2: Upload the modified zip to S3 and get the file URL
        set_aws_credentials()
        s3_file_url = upload_to_s3(modified_zip_path)

        if s3_file_url:
            # Step 3: Prepare JSON based on provided data
            json_data = prepare_json(
                resource_id=resource_id,
                title=title,
                duration=duration,
                parent_id=parent_id,
                child_order=child_order
            )

            # Create a spreadsheet name
            spread_sheet_name = f"{title} - {resource_id}"
            upload_to_google_sheets(json_data, spread_sheet_name)

            # Final JSON structure to send with the request
            final_json = {
                "spread_sheet_name": spread_sheet_name,
                "data_sets_to_be_loaded": [
                    "ResourcesData",
                    "Units",
                    "QuestionSet"
                ],
                "question_set_questions_dir_path_url": s3_file_url,
                "is_json_converted": False
            }
            submit_sheet_loading_request(final_json)
            return submit_unlock_request(resource_id)

        else:
            return HttpResponse("Failed to upload file to S3.", status=500)

    return render(request, 'Coding_Practice/upload_form.html')


