import os
from datetime import datetime 
import json 

import anvil.server
from anvil.files import data_files
from anvil.tables import app_tables

from yoti_python_sdk import Client
from yoti_python_sdk.dynamic_sharing_service.policy import DynamicPolicyBuilder
from yoti_python_sdk.dynamic_sharing_service import (
    DynamicScenarioBuilder,
    create_share_url
)

# Configuration
YOTI_CLIENT_SDK_ID = '754182a1-fbf6-4a20-8615-cf4666f964cc'
YOTI_PRIVATE_KEY_PATH = data_files['Yoti-For-Kaimai-access-security.pem']
CALLBACK_URL = "https://reliable-equatorial-heron.anvil.app/_/api/yoti-callback"

# Examine private key before client initialization
print("=== EXAMINING PRIVATE KEY ===")
try:
    with open(YOTI_PRIVATE_KEY_PATH, 'r') as f:
        key_content = f.read()
        print("Key file exists and can be read")
        print("First 100 chars of key:", key_content[:100])
        print("Key length:", len(key_content))
except Exception as key_error:
    print("Error reading key file:", str(key_error))

# Initialize Yoti client
print("=== INITIALIZING YOTI CLIENT ===")
try:
    print(f"SDK ID: {YOTI_CLIENT_SDK_ID}")
    print(f"Key path exists: {os.path.exists(YOTI_PRIVATE_KEY_PATH)}")
    yoti_client = Client(YOTI_CLIENT_SDK_ID, YOTI_PRIVATE_KEY_PATH)
    print("Yoti client initialized successfully")
except Exception as client_error:
    print("Error initializing Yoti client:", str(client_error))
    raise

@anvil.server.callable
def yoti_session():
    print('Hit yoti session')
    try:
        # Create policy
        print("Creating policy...")
        policy = (DynamicPolicyBuilder()
            .with_full_name()
            .with_email()
            .build())
        print("Policy created:", policy.to_json())
        
        # Create scenario
        print("Creating scenario...")
        scenario = (DynamicScenarioBuilder()
            .with_policy(policy)
            .with_callback_endpoint(CALLBACK_URL)
            .build())
        print("Scenario created:", scenario.to_json())
        
        # Create share URL
        print("Creating share URL...")
        share_url = create_share_url(yoti_client, scenario)
        actual_url = share_url.share_url
        print("Share URL created:", actual_url)
        
        return {
            "clientSdkId": YOTI_CLIENT_SDK_ID,
            "shareUrl": actual_url
        }
    except Exception as e:
        print("Error in yoti_session:", str(e))
        import traceback
        print(traceback.format_exc())
        raise


