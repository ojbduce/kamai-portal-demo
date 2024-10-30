
import anvil.server
import anvil.users
import anvil.tables as tables
from anvil.tables import app_tables
from yoti_python_sdk.client import Client
from yoti_python_sdk.share_url.policy import DynamicPolicyBuilder
from yoti_python_sdk.share_url.builder import DynamicScenarioBuilder

# Initialize the Yoti Client with SDK ID and private key
YOTI_CLIENT_SDK_ID = 'your_sdk_id'
YOTI_PRIVATE_KEY_PATH = '_/theme/keys/Yoti-For-Kaimai-access-security.pem'
yoti_client = Client(YOTI_CLIENT_SDK_ID, YOTI_PRIVATE_KEY_PATH)

@anvil.server.callable
def generate_yoti_qr_code():
    # Define the policy to request Yoti attributes
    policy = (DynamicPolicyBuilder()
        .with_full_name()
        .with_email()
        .with_remember_me_id()
        .build())

    # Create a dynamic scenario with the policy
    scenario = (DynamicScenarioBuilder()
        .with_policy(policy)
        .for_application(YOTI_CLIENT_SDK_ID)
        .build())

    # Generate the share URL (this URL will be used to create the QR code)
    share_url = yoti_client.create_share_url(scenario)
    
    # Return the share URL to the client-side to generate the QR code
    return share_url



