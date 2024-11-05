import os
from datetime import datetime 
import json 

import anvil.server
import anvil.users
from anvil.files import data_files
import anvil.tables as tables
from anvil.tables import app_tables

from yoti_python_sdk import Client
from yoti_python_sdk.dynamic_sharing_service.policy import DynamicPolicyBuilder
from yoti_python_sdk.dynamic_sharing_service import (
    DynamicScenarioBuilder,
    create_share_url
)

import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
YOTI_CLIENT_SDK_ID = '754182a1-fbf6-4a20-8615-cf4666f964cc'
YOTI_PRIVATE_KEY_PATH = data_files['Yoti-For-Kaimai-access-security.pem']
ALLOWED_ORIGINS = ["https://reliable-equatorial-heron.anvil.app"]
CALLBACK_URL = f"{ALLOWED_ORIGINS[0]}/_/api/yoti-callback"

# Initialize Yoti client
try:
    print("Initializing Yoti client...")
    print(f"SDK ID: {YOTI_CLIENT_SDK_ID}")
    print(f"Key path exists: {os.path.exists(YOTI_PRIVATE_KEY_PATH)}")
    yoti_client = Client(YOTI_CLIENT_SDK_ID, YOTI_PRIVATE_KEY_PATH)
    print("Yoti client initialized successfully")
except Exception as client_error:
    print("Error initializing Yoti client:", str(client_error))
    raise

def validate_yoti_setup():
    """Validate Yoti configuration and key files."""
    logger.info("Validating Yoti setup...")
    
    if not YOTI_CLIENT_SDK_ID:
        logger.error("YOTI_CLIENT_SDK_ID is not set")
        raise ValueError("YOTI_CLIENT_SDK_ID is not set")
    
    logger.info(f"Checking private key at: {YOTI_PRIVATE_KEY_PATH}")
    if not os.path.exists(YOTI_PRIVATE_KEY_PATH):
        logger.error(f"Private key file not found at: {YOTI_PRIVATE_KEY_PATH}")
        raise ValueError(f"Private key file not found at: {YOTI_PRIVATE_KEY_PATH}")
    
    try:
        with open(YOTI_PRIVATE_KEY_PATH, 'r') as f:
            key_content = f.read()
            if not key_content.startswith('-----BEGIN RSA PRIVATE KEY-----'):
                logger.error("Invalid private key format")
                raise ValueError("Invalid private key format")
            logger.info("Private key format validated")
    except Exception as e:
        logger.error(f"Error reading private key: {str(e)}")
        raise ValueError(f"Error reading private key: {str(e)}")
    
    logger.info("Yoti setup validation complete")

@anvil.server.http_endpoint("/sessions", methods=["POST", "OPTIONS"])
def create_session():
    """Create a new Yoti session and return share URL."""
    logger.info(f"=== CREATE SESSION ENDPOINT HIT ===")
    logger.info(f"Method: {anvil.server.request.method}")
    logger.info(f"Headers: {dict(anvil.server.request.headers)}")
    logger.info(f"Origin: {anvil.server.request.origin}")
    
    if anvil.server.request.method == "OPTIONS":
        logger.info("Handling OPTIONS preflight request")
        return handle_preflight()
    
    try:
        # Validate origin
        if anvil.server.request.origin not in ALLOWED_ORIGINS:
            logger.error(f"Invalid origin: {anvil.server.request.origin}")
            return anvil.server.HttpResponse(
                403,
                body={"error": "Invalid origin"}
            )
        
        # Generate session data
        logger.info("Calling yoti_session()")
        response_data = yoti_session()
        logger.info(f"Response data generated: {response_data}")
        
        # Return success response
        return anvil.server.HttpResponse(
            200,
            headers={
                "Access-Control-Allow-Origin": anvil.server.request.origin,
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
                "Content-Type": "application/json"
            },
            body=response_data
        )
    except Exception as e:
        logger.error("=== ERROR IN CREATE SESSION ===")
        logger.error(f"Error type: {type(e)}")
        logger.error(f"Error message: {str(e)}")
        logger.error("Stack trace:")
        logger.error(traceback.format_exc())
        
        error_response = {
            "error": str(e),
            "details": traceback.format_exc()
        }
        
        return anvil.server.HttpResponse(
            500,
            headers={
                "Access-Control-Allow-Origin": anvil.server.request.origin,
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
                "Content-Type": "application/json"
            },
            body=error_response
        )

def handle_preflight():
    """Handle CORS preflight requests."""
    return anvil.server.HttpResponse(
        200,
        headers={
            "Access-Control-Allow-Origin": anvil.server.request.origin,
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }
    )

@anvil.server.callable
def yoti_session():
    print('Hit yoti session')
    try:
        # Create policy with debug output
        print("Creating policy...")
        policy = (DynamicPolicyBuilder()
            .with_full_name()
            .with_email()
            .build())
        print("Policy JSON:", policy.to_json())
        
        # Create scenario with debug output
        print("Creating scenario...")
        scenario = (DynamicScenarioBuilder()
            .with_policy(policy)
            .with_callback_endpoint(CALLBACK_URL)
            .build())
        print("Scenario JSON:", scenario.to_json())
        
        # Create share URL with debug output
        print("Creating share URL...")
        try:
            share_url = create_share_url(yoti_client, scenario)
            print("Share URL created successfully")
        except Exception as share_error:
            print("Error in create_share_url:")
            print("Scenario data:", json.dumps(scenario.to_json(), indent=2))
            print("Error:", str(share_error))
            raise
            
        actual_url = share_url.url
        print("Generated URL:", actual_url)
        
        return {
            "clientSdkId": YOTI_CLIENT_SDK_ID,
            "shareUrl": actual_url
        }
    except Exception as e:
        print("Error creating share session:", str(e))
        raise

@anvil.server.route("/yoti-callback", methods=["POST"])
def yoti_callback():
    """Handle Yoti callback after successful authentication."""
    print("Received Yoti callback")
    try:
        token = anvil.server.request.body_json.get("token")
        print(f"Received token: {token}")
        # TODO: Process token and handle user authentication
        # TODO: Implement user session management
    except Exception as e:
        print(f"Error processing Yoti callback: {e}")
        raise

# Fallback for Anvil Data Files Service
@anvil.server.callable
def yoti_get_keys():
    """Fallback method to retrieve Yoti keys from Anvil tables."""
    print("Attempting to retrieve Yoti keys from tables")
    keys_row = app_tables.files.get(name='yoti_keys')
    if keys_row:
        keys_file = keys_row['file'].get_bytes().decode('utf-8')
        print("Retrieved key file (first 100 chars):", keys_file[:100])
        
        tmp_keys_path = '/tmp/yoti_keys.pem'
        with open(tmp_keys_path, 'wb') as keys:
            keys.write(keys_file.encode('utf-8'))
            return yoti_session(tmp_keys_path)
            
    return "Keys not found"

