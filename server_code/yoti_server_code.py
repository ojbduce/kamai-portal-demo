import anvil.server
import anvil.users
from anvil.files import data_files
import os
from datetime import datetime 
import uuid
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
YOTI_PRIVATE_KEY_PATH = data_files['Yoti-For-Kaimai-access-security.pem']
#/tmp/anvil-data-files/table-866054/Yoti-For-Kaimai-access-security.pem
yoti_client = Client(YOTI_CLIENT_SDK_ID,YOTI_PRIVATE_KEY_PATH)

# @anvil.server.callable
# def create_yoti_share_session():
#     yoti_client = Client(YOTI_CLIENT_SDK_ID, YOTI_PRIVATE_KEY_PATH)
#     policy = DynamicPolicyBuilder().with_full_name().with_email().build()
#     scenario = DynamicScenarioBuilder().with_policy(policy).with_callback_endpoint("https://your-app.anvil.app/yoti-callback").build()
#     share_url = create_share_url(yoti_client, scenario)
#     yoti_session_id = share_url.share_url.split('/')[-1]
#     # Return the session data as a dictionary
#     return {"clientSdkId": YOTI_CLIENT_SDK_ID, "shareUrl": share_url.share_url}

@anvil.server.http_endpoint("/sessions", methods=["POST", "OPTIONS"])
def create_session():
    print("Hit create session")
    response_data = yoti_session()
    print("Response data:", response_data)  
    allowed_origins = ["https://reliable-equatorial-heron.anvil.app"]
    response_headers = {}
    if anvil.server.request.origin in allowed_origins:
      response_headers["Access-Control-Allow-Origin"] = anvil.server.request.origin
      response_headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
      response_headers["Access-Control-Allow-Headers"] = "Content-Type"
      return anvil.server.HttpResponse(
        200,
        headers=response_headers,
        body=response_data
      )

# Add this function to validate your setup
def validate_yoti_setup():
    if not YOTI_CLIENT_SDK_ID:
        raise ValueError("YOTI_CLIENT_SDK_ID is not set")
    
    if not os.path.exists(YOTI_PRIVATE_KEY_PATH):
        raise ValueError(f"Private key file not found at: {YOTI_PRIVATE_KEY_PATH}")
    
    try:
        with open(YOTI_PRIVATE_KEY_PATH, 'r') as f:
            key_content = f.read()
            if not key_content.startswith('-----BEGIN RSA PRIVATE KEY-----'):
                raise ValueError("Invalid private key format")
    except Exception as e:
        raise ValueError(f"Error reading private key: {str(e)}")

@anvil.server.callable
def yoti_session():
    print('Hit yoti session')
    try:
        # Validate setup first
        validate_yoti_setup()
        
        yoti_client = Client(YOTI_CLIENT_SDK_ID, YOTI_PRIVATE_KEY_PATH)
        policy = (DynamicPolicyBuilder()
          .with_full_name()
          .with_email()
          .build())
        scenario = (DynamicScenarioBuilder()
          .with_policy(policy)
          .with_callback_endpoint("https://reliable-equatorial-heron.anvil.app/_/api/yoti-callback")
          .build())
        
        share_url = create_share_url(yoti_client, scenario)
        # Access the actual URL string using .url attribute
        actual_url = share_url.url
        print("Generated share URL:", actual_url)
        session_id = actual_url.split('/')[-1]
        
        time = datetime.now()
        app_tables.sessions.add_row(time_date=time, yoti_session_id=session_id)
        
        return {
          "sessionId": session_id
        }
    except Exception as e:
        print(f"Error creating share session: {str(e)}")
        # Add more detailed error logging
        import traceback
        print(traceback.format_exc())
        raise  # Re-raise the exception to see the full error
    

  

@anvil.server.route("/yoti-callback", methods=["POST"])
def yoti_callback():
    print("Hit callback")
    try:
        yoti_client = Client(YOTI_CLIENT_SDK_ID, YOTI_PRIVATE_KEY_PATH) #?
        token = anvil.server.request.body_json.get("token")
        print(f"Token:{token}")
    
        # activity_details = yoti_client.get_activity_details(token)
        
        # profile = activity_details.user_profile
        # full_name = profile.get("full_name", None)
        # email = profile.get("email_address", None)
        # print(f"User Full Name: {full_name}, Email: {email}")
        
        # # Store or process the profile data as needed
        # app_tables.users.add_row(full_name=full_name, email=email, timestamp=datetime.now())
        # print("profile received")
        # return anvil.server.HttpResponse(200, body="Profile received")
    except Exception as e:
        print(f"Error retrieving token: {e}")
        # print(f"Error retrieving profile: {e}")
        # return anvil.server.HttpResponse(500, body="Error processing callback")
    



    
@anvil.server.callable
def yoti_get_keys():
  print("Function yoti_get_keys called")
  keys_row = app_tables.files.get(name='yoti_keys')
  print(keys_row)#remove
  if keys_row:
    keys_file = keys_row['file'].get_bytes().decode('utf-8')
    print(keys_file[:100])  
    tmp_keys_path = '/tmp/yoti_keys.pem' #just use path from data files service why not working?
    with open (tmp_keys_path, 'wb') as keys:
      keys.write(keys_file)
      print('keys')
      yoti_session(tmp_keys_path)
  else:
    return "Keys not found"
   

# # Debugging Missing pem file Version
# @anvil.server.callable
# def generate_yoti_qr_code():
#   pem_row = app_tables.files.get(name='yoti_keys')
#   print(pem_row)
#   if pem_row:
#     print("PEM row found:", pem_row)
#     print("Name column:", pem_row['name'])
#     print("File column:", pem_row['file'])
#     if pem_row['file']:
#       print("PEM file is present in the row.")
#       return pem_row['file'].get_bytes().decode('utf-8')  # Decode for testing
#     else:
#       print("PEM file column is empty or missing.")
#       return "PEM file column is empty or missing."
#   else:
#     print("PEM row not found.")
#     return "PEM row not found."
#     pem_content = pem_row['file'].get_bytes()
#     temp_pem_path = '/tmp/yoti_private_key.pem'

#     #New function

#     # Write the PEM content to the temporary file
#     with open(temp_pem_path, 'wb') as pem_file:
#         pem_file.write(pem_content)
#     yoti_client = Client(YOTI_CLIENT_SDK_ID, temp_pem_path)
#     try:
#         policy = (DynamicPolicyBuilder()
#             .with_full_name()
#             .with_email()
#             .build())
        
#         scenario = (DynamicScenarioBuilder()
#             .with_policy(policy)
#             .with_callback_endpoint("_/api/yoti-callback")
#             .build())

#         share_url = create_share_url(yoti_client,scenario)
#         print (share_url.share_url)
#         return share_url.share_url
        

#     except Exception as e:
#         print(f"Error creating share session: {e}")
#         return "Error creating share session."
#     if not pem_row or 'file' not in pem_row:
#         print("PEM file not found in Data Table.")


#     pem_content = pem_row['file'].get_bytes()

#     temp_pem_path = '/tmp/yoti_private_key.pem'

#     # Write the PEM content to the temporary file
#     with open(temp_pem_path, 'wb') as pem_file:
#         pem_file.write(pem_content)

#     yoti_client = Client(YOTI_CLIENT_SDK_ID, temp_pem_path)
#     try:
#         policy = (DynamicPolicyBuilder()
#             .with_full_name()
#             .with_email()
#             .build())
        
#         scenario = (DynamicScenarioBuilder()
#             .with_policy(policy)
#             .with_callback_endpoint("/yoti/auth")
#             .build())

#         share_url = yoti_client.create_share_url(scenario)
#         print("Generated share URL:", share_url)
#         return share_url.share_url

#     except Exception as e:
#         print(f"Error creating share session: {e}")
#         return "Error creating share session."

#     finally:
#         # Clean up the temporary file (optional but recommended for security)
#         os.remove(temp_pem_path)















# @anvil.server.callable
# def generate_yoti_qr_code():
#     try:
#         pem_row = app_tables.files.get(name='yoti_keys')
#         if not pem_row or 'file' not in pem_row:
#             raise RuntimeError("PEM file not found in Data Table.")
        
#         # Define the temporary path and write the file content once
#         temp_pem_path = '/tmp/yoti_private_key.pem'
#         with open(temp_pem_path, 'wb') as pem_file:
#             pem_file.write(pem_row['file'].get_bytes())

#         yoti_client = Client(YOTI_CLIENT_SDK_ID, temp_pem_path)

#         # Define policy and scenario as before
#         policy = (DynamicPolicyBuilder()
#             .with_full_name()
#             .with_email()
#           
#             .build())
        
#         scenario = (DynamicScenarioBuilder()
#             .with_policy(policy)
#             .for_application(YOTI_CLIENT_SDK_ID)
#             .build())

#         share_url = yoti_client.create_share_url(scenario)
#         return share_url.share_url

#     except Exception as e:
#         print(f"Error creating share session: {e}")
#         return "Error creating share session."

#     finally:
#         # Clean up the temporary file
#         if os.path.exists(temp_pem_path):
#             os.remove(temp_pem_path)





# @anvil.server.callable
# def generate_yoti_qr_code():
#     try:
#         # Retrieve the PEM file from the Data Table
#         pem_row = app_tables.files.get(name='yoti_keys')
#         if not pem_row or 'file' not in pem_row:
#             raise RuntimeError("PEM file not found in Data Table.")
        
#         # Get the binary content of the PEM file
#         private_key = pem_row['file'].get_bytes()  # Keeps the PEM file as binary bytes
        
#         # Initialize the Yoti Client with the private key bytes if Yoti SDK supports it
#         yoti_client = Client(YOTI_CLIENT_SDK_ID, private_key)

#         # Define the policy and scenario
#         policy = (DynamicPolicyBuilder()
#             .with_full_name()
#             .with_email()
#            
#             .build())
        
#         scenario = (DynamicScenarioBuilder()
#             .with_policy(policy)
#             .for_application(YOTI_CLIENT_SDK_ID)
#             .build())

#         # Generate and return the share URL
#         share_url = yoti_client.create_share_url(scenario)
#         return share_url.share_url

#     except Exception as e:
#         print(f"Error creating share session: {e}")
#         return "Error creating share session."


# #@anvil.server.callable
# #def generate_yoti_qr_code():
#     # Retrieve the PEM file from the Data Table
#   pem_row = app_tables.files.get(name='yoti_keys')
#   print(pem_row)
#   if pem_row:
#     print("PEM row found:", pem_row)
#     #print("Name column:", pem_row['name'])
#   #   print("File column:", pem_row['file'])
#   #   # Check specifically for the 'file' column
#   #   if pem_row['file']:
#   #     print("PEM file is present in the row.")
#   #     return pem_row['file'].get_bytes().decode('utf-8')  # Decode for testing
#   #   else:
#   #     print("PEM file column is empty or missing.")
#   #     return "PEM file column is empty or missing."
#   # else:
#   #   print("PEM row not found.")
#   #   return "PEM row not found."
#     pem_content = pem_row['file'].get_bytes()

#     # Define a temporary file path in the /tmp directory
#     temp_pem_path = '/tmp/yoti_private_key.pem'

#     # Write the PEM content to the temporary file
#     with open(temp_pem_path, 'wb') as pem_file:
#         pem_file.write(pem_content)
#     yoti_client = Client(YOTI_CLIENT_SDK_ID, temp_pem_path)
#     try:
#         policy = (DynamicPolicyBuilder()
#             .with_full_name()
#             .with_email()
#             .build())
        
#         scenario = (DynamicScenarioBuilder()
#             .with_policy(policy)
#             .with_callback_endpoint("/yoti-callback")
#             .build())

#         share_url = create_share_url(yoti_client,scenario)
#         print (share_url.share_url)
#         return share_url.share_url
        

#     except Exception as e:
#         print(f"Error creating share session: {e}")
#         return "Error creating share session."
#     if not pem_row or 'file' not in pem_row:
#         print("PEM file not found in Data Table.")
  
#     pem_content = pem_row['file'].get_bytes()

#     temp_pem_path = '/tmp/yoti_private_key.pem'

#     # Write the PEM content to the temporary file
#     with open(temp_pem_path, 'wb') as pem_file:
#         pem_file.write(pem_content)

#     yoti_client = Client(YOTI_CLIENT_SDK_ID, temp_pem_path)
#     try:
#         policy = (DynamicPolicyBuilder()
#             .with_full_name()
#             .with_email()
#             .build())
        
#         scenario = (DynamicScenarioBuilder()
#             .with_policy(policy)
#             .with_callback_endpoint("/yoti/auth")
#             .build())

#         share_url = yoti_client.create_share_url(scenario)
#         print("Generated share URL:", share_url)
#         return share_url.share_url

#     except Exception as e:
#         print(f"Error creating share session: {e}")
#         return "Error creating share session."

#     finally:
#         # Clean up the temporary file (optional but recommended for security)
#         os.remove(temp_pem_path)


