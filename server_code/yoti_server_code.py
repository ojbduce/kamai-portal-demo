import anvil.files
from anvil.files import data_files

import anvil.server
import anvil.users
import os
import anvil.tables as tables
from anvil.tables import app_tables
from yoti_python_sdk import Client
from yoti_python_sdk.dynamic_sharing_service.policy import (
    DynamicPolicyBuilder,
    SourceConstraintBuilder,
)
from yoti_python_sdk.dynamic_sharing_service import DynamicScenarioBuilder
from yoti_python_sdk.dynamic_sharing_service import create_share_url

YOTI_CLIENT_SDK_ID = '754182a1-fbf6-4a20-8615-cf4666f964cc'
#YOTI_PRIVATE_KEY_PATH = '/tmp/anvil-data-files/table-864896/Yoti-For-Kaimai-access-security.pem'
#yoti_client = Client(YOTI_CLIENT_SDK_ID,YOTI_PRIVATE_KEY_PATH)

@anvil.server.route("/yoti-callback")
def yoti_logged_in(**p):
    print('logged-in')
    return anvil.server.FormResponse("Main_Copy")

@anvil.server.callable
def generate_yoti_qr_code():
    # Retrieve the PEM file from the Data Table
    pem_row = app_tables.Files.get(name='yoti_keys')
    if not pem_row or 'file' not in pem_row:
        raise RuntimeError("PEM file not found in Data Table.")
    
    # Get the file contents as bytes
    pem_content = pem_row['file'].get_bytes()

    # Define a temporary file path in the /tmp directory
    temp_pem_path = '/tmp/yoti_private_key.pem'

    # Write the PEM content to the temporary file
    with open(temp_pem_path, 'wb') as pem_file:
        pem_file.write(pem_content)

    # Initialize the Yoti Client with the temporary file path
    yoti_client = Client(YOTI_CLIENT_SDK_ID, temp_pem_path)

    # Proceed with the rest of your code (e.g., creating the share URL)
    # Define the policy and scenario
    try:
        policy = (DynamicPolicyBuilder()
            .with_full_name()
            .with_email()
            .with_remember_me_id()
            .build())
        
        scenario = (DynamicScenarioBuilder()
            .with_policy(policy)
            .for_application(YOTI_CLIENT_SDK_ID)
            .build())

        share_url = yoti_client.create_share_url(scenario)
        print("Generated share URL:", share_url)
        return share_url

    except Exception as e:
        print(f"Error creating share session: {e}")
        return "Error creating share session."

    finally:
        # Clean up the temporary file (optional but recommended for security)
        os.remove(temp_pem_path)
    if not pem_row or 'file' not in pem_row:
        print("PEM file not found in Data Table.")
    
    # Get the file contents as bytes
    pem_content = pem_row['file'].get_bytes()

    # Define a temporary file path in the /tmp directory
    temp_pem_path = '/tmp/yoti_private_key.pem'

    # Write the PEM content to the temporary file
    with open(temp_pem_path, 'wb') as pem_file:
        pem_file.write(pem_content)

    # Initialize the Yoti Client with the temporary file path
    yoti_client = Client(YOTI_CLIENT_SDK_ID, temp_pem_path)

    # Proceed with the rest of your code (e.g., creating the share URL)
    # Define the policy and scenario
    try:
        policy = (DynamicPolicyBuilder()
            .with_full_name()
            .with_email()
            .with_remember_me_id()
            .build())
        
        scenario = (DynamicScenarioBuilder()
            .with_policy(policy)
            .for_application(YOTI_CLIENT_SDK_ID)
            .build())

        share_url = yoti_client.create_share_url(scenario)
        print("Generated share URL:", share_url)
        return share_url

    except Exception as e:
        print(f"Error creating share session: {e}")
        return "Error creating share session."

    finally:
        # Clean up the temporary file (optional but recommended for security)
        os.remove(temp_pem_path)


