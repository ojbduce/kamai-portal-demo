import anvil.files
from anvil.files import data_files

import anvil.server
import anvil.users
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
YOTI_PRIVATE_KEY_PATH = '/tmp/anvil-data-files/table-864896/Yoti-For-Kaimai-access-security.pem'
yoti_client = Client(YOTI_CLIENT_SDK_ID,YOTI_PRIVATE_KEY_PATH)

@anvil.server.route("/yoti-callback")
def yoti_logged_in(**p):
    print('logged-in')
    return anvil.server.FormResponse("Main_Copy")

@anvil.server.callable
def generate_yoti_qr_code():
    try:
        pem_row = app_tables.files.get(name='Yoti-For-Kaimai-access-security.pem')
        if not pem_row or 'file' not in pem_row:
            raise RuntimeError("PEM file not found in Data Table.")
            print("PEM file not found in Data Table.")
            return "Error with keys"
        
        # Read the PEM file content from the Data Table
        private_key = pem_row['file'].get_bytes().decode('utf-8')
    @anvil.server.callable
def generate_yoti_qr_code(message=None):
    print(f"Received message: {message}")  # This is optional and for testing purposes
    
    # Retrieve the PEM file from the Data Table
    pem_row = app_tables.files.get(name='Yoti-For-Kaimai-access-security.pem')
    if not pem_row or 'file' not in pem_row:
        print("PEM file not found in Data Table.")
        return "Error with keys"

    try:
        # Initialize the Yoti Client as before
        private_key = pem_row['file'].get_bytes().decode('utf-8')
        yoti_client = Client(YOTI_CLIENT_SDK_ID, private_key)

        # Define the policy and generate the share URL
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
        return share_url

    except Exception as e:
        print(f"Error creating share session: {e}")
        return "Error creating share session."



