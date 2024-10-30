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
    client = Client(YOTI_CLIENT_SDK_ID, YOTI_PRIVATE_KEY_PATH)
    policy = (DynamicPolicyBuilder()
        .with_full_name()
        .with_email()
        .build())

    # Create a dynamic scenario with the policy
    scenario = (DynamicScenarioBuilder()
        .with_policy(policy)
        .with_callback_endpoint("/yoti-callback")
        .build())

    # Generate the share URL (this URL will be used to create the QR code)
    try:
      share_url = create_share_url(client,scenario)
      print("Generated share URL:", share_url)
      print (share_url.share_url)
      #print(dir(share_url))
      return share_url.share_url
    except Exception as e:
      print(f"Error creating share session: {e}")
      return None



