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
# In assets
#YOTI_PRIVATE_KEY_PATH='_/theme/Yoti-For-Kaimai-access-security.pem'

@anvil.server.route("/yoti-callback")
def yoti_logged_in(**p):
    print('logged-in')
    return anvil.server.FormResponse("Main_Copy")


@anvil.server.callable
def yoti_get_keys():
  keys_row = app_tables.files.get(name='keys')
  if keys_row:
    print(keys_row)#remove
    keys_file = keys_row['file'].get_bytes()
    tmp_keys_path = '/tmp/yoti_keys'
    with open (tmp_keys_path, 'wb') as keys:
      keys.write(keys_file)
    return tmp_keys_path
  else:
    return "Keys not found"
    #raise RuntimeError("PEM file not found in Data Table.")

@anvil.server.callable
def yoti_session(tmp_keys_path):
  get_keys()
  yoti_client = Client(YOTI_CLIENT_SDK_ID, tmp_keys_path)
  try:
    policy = (DynamicPolicyBuilder()
      .with_full_name()
      .with_email()
      .build())
    scenario = (DynamicScenarioBuilder()
      .with_policy(policy)
      .with_callback_endpoint("/yoti-callback")
      .build())
    share_url = create_share_url(yoti_client,scenario)
    print("Generated share URL:", share_url.share_url)
    return share_url.share_url
  except Exception as e:
      print(f"Error creating share session: {e}")#remove
      return "Error creating share session."



  except Exception as e:
      print(f"Error creating share session: {e}")
      return "Error creating share session."

  finally:
      # Clean up the temporary file (optional but recommended for security)
      os.remove(temp_pem_path)

  


@anvil.server.callable
def generate_yoti_qr_code():
    # Retrieve the PEM file from the Data Table
  pem_row = app_tables.files.get(name='yoti_keys')
  print(pem_row)
  if pem_row:
    print("PEM row found:", pem_row)
    #print("Name column:", pem_row['name'])
  #   print("File column:", pem_row['file'])
  #   # Check specifically for the 'file' column
  #   if pem_row['file']:
  #     print("PEM file is present in the row.")
  #     return pem_row['file'].get_bytes().decode('utf-8')  # Decode for testing
  #   else:
  #     print("PEM file column is empty or missing.")
  #     return "PEM file column is empty or missing."
  # else:
  #   print("PEM row not found.")
  #   return "PEM row not found."
    pem_content = pem_row['file'].get_bytes()

    # Define a temporary file path in the /tmp directory
    temp_pem_path = '/tmp/yoti_private_key.pem'

    #New function

    # Write the PEM content to the temporary file
    with open(temp_pem_path, 'wb') as pem_file:
        pem_file.write(pem_content)
    yoti_client = Client(YOTI_CLIENT_SDK_ID, temp_pem_path)
    try:
        policy = (DynamicPolicyBuilder()
            .with_full_name()
            .with_email()
            .build())
        
        scenario = (DynamicScenarioBuilder()
            .with_policy(policy)
            .with_callback_endpoint("/yoti-callback")
            .build())

        share_url = create_share_url(yoti_client,scenario)
        print (share_url.share_url)
        return share_url.share_url
        

    except Exception as e:
        print(f"Error creating share session: {e}")
        return "Error creating share session."
    if not pem_row or 'file' not in pem_row:
        print("PEM file not found in Data Table.")
  
    pem_content = pem_row['file'].get_bytes()

    temp_pem_path = '/tmp/yoti_private_key.pem'

    # Write the PEM content to the temporary file
    with open(temp_pem_path, 'wb') as pem_file:
        pem_file.write(pem_content)

    yoti_client = Client(YOTI_CLIENT_SDK_ID, temp_pem_path)
    try:
        policy = (DynamicPolicyBuilder()
            .with_full_name()
            .with_email()
            .build())
        
        scenario = (DynamicScenarioBuilder()
            .with_policy(policy)
            .with_callback_endpoint("/yoti/auth")
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
#         return share_url

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
#         return share_url

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
#         return share_url

#     except Exception as e:
#         print(f"Error creating share session: {e}")
#         return "Error creating share session."

#     finally:
#         # Clean up the temporary file (optional but recommended for security)
#         os.remove(temp_pem_path)


