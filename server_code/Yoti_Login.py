import anvil.secrets
import anvil.server
import anvil.users
import requests
from anvil.files import data_files
import os
from datetime import datetime 
import uuid
import anvil.tables as tables
from anvil.tables import app_tables
import bcrypt
import secrets


@anvil.server.callable
def return_remember_me_id():
  return anvil.server.get['remember_me_id']

@anvil.server.callable
def force_login_user():
  print(f"force_login: user row object from session {anvil.server.session['current_user_row']}")
  user = anvil.server.session['current_user_row']
  return user

@anvil.server.callable 
def create_new_user(remember_me_id, verification_date,email):
  import base64
  print("create_new_user: Creating new User. Accessing system password.")
  system_password = anvil.secrets.get_secret("system_password")
  print("create_new_user:Hashing password.")
  hash_password = bcrypt.hashpw(system_password.encode('utf-8'), bcrypt.gensalt())
  print(f"create_new_user: bcrypt hash is of type: {type(hash_password)}")
  #Ok so we convert it.
  password_hash = base64.b64encode(hash_password).decode('utf-8')
  print("create_new_user. Password hashed. Adding User to Users Table.")
  user = app_tables.users.add_row(
    remember_me_id=remember_me_id, 
    verification_date= verification_date,
    email=email,
    enabled=True,
    password_hash=password_hash)
  print("create_new_user: Try force_login from here...")
  anvil.users.force_login(user) #the row object
  current_user_row = app_tables.people.users(remember_me_id=remember_me_id)
  anvil.server.session['current_user_row'] = current_user_row
  print("create_new_user: User data received and added to the Users Table. Current row for rem_id in server session")
  print("Testing Users Service login:")
  user = app_tables.users.get(remember_me_id=remember_me_id)
  return user

#login_yoti
'''Part of the external verification pipeline. 
Takes an id received from the api. Not called Client-sde, atm'''
@anvil.server.callable
def login_yoti(remember_me_id,verification_date, email):
    import base64
    print(f"Hit login with ID{remember_me_id}")
    #check for existing user
    user = app_tables.users.get(remember_me_id=remember_me_id)
    system_password = anvil.secrets.get_secret('system_password')
    if user is not None:
      password_hash = base64.b64decode(user['password_hash'])
      if bcrypt.checkpw(system_password.encode('utf-8'), password_hash):
        anvil.users.force_login(user)
      #logging remove later
        users_service_test = anvil.users.get_user(allow_remembered=True) # test server-side, since client side None
        print(f"Anvil Users Service force_login test: user row object? {users_service_test}")#OK
        print(f"Anvil Users actual user/id check: {anvil.users.get_user()['remember_me_id']}")#OK
        print(f"Existing Yoti User {remember_me_id} is logged-in")#OK
        anvil.server.session['remember_me_id'] = remember_me_id # as Users not working Client-side
        print(f"login_yoti. Server-side success - remember_me_id from server session {anvil.server.session}")
        return user
      else:
        print("create_new_user: password verification failed")
        return None
    else:
      create_new_user(remember_me_id,verification_date,email)
      return user
    
#Main Function
@anvil.server.http_endpoint("/yka", methods=["POST"], enable_cors=True)
def receive_user_details():
    print("Hit users endpoint!")
    userData = anvil.server.request.body_json
    print(f"Data Received: {bool(userData)}")  
    print(f"Keys received: {userData.keys()}")  
    print(f"Data dump: {userData}")  
    if not all(key in userData for key in ['email', 'rememberMeId', 'verificationDate']):
        return {"status": "error", "message": "Missing required fields"}, 400
    print("All data available. Adding to the Data Table")
    email = userData['email']
    print(f"Test printing email address: {email}")
    remember_me_id = userData['rememberMeId']
    verification_date = datetime.now()
  #split here. Split for testing version but log-in can be a separate function.
    existing_user = app_tables.users.search(remember_me_id=remember_me_id)
    if existing_user:
      try:
        login_yoti(remember_me_id,verification_date, email)
        return {"status": "success", "message": "Existing user logged in"}
      except Exception as e:
        print(f"login_yoti_failed {e}")
        return {"status": "error", "message": str(e)}, 500
    else:#create new user
      try:
          create_new_user(remember_me_id,verification_date,email)
          new_user = app_tables.users.search(remember_me_id=remember_me_id)
          if new_user is not None:
            login_yoti(remember_me_id,verification_date, email) 
            return {"status": "success", "message": "User added successfully"}
          else:
            print("receive_user_data:new user failed")
          # no point in breaking the verification/appearence
          return {"status": "success", "message": "User added successfully"}
      except Exception as e:
          print(f"Error adding to Data Table: {e}") 
          return {"status": "error", "message": str(e)}, 500



     
 

















@anvil.server.http_endpoint("/sessions", methods=["POST"])
def create_session():
    print("Hit create session")
    sessionId = SESSION_ID
  #immediately return session_ID
    try:
        context = yoti_session() #currently the .share_url variety
        # if not share_url:
        #     print("No share_url returned from yoti_session")
        #     return anvil.server.HttpResponse(500, body={"error": "Failed to create session"})
            
        print(f"Printing context from create_session: {context}")
        print(f"share_url type: {type(context)}")  # Debug the object type
        
        # Previous approach (commented for reference)
        # sessionID = share_url.ref_id
        # print(f"Session ID (ref_id): {sessionID}")
        
        # New approach: try using QR code URL
        #sessionID = getattr(share_url, '_ShareUrl__qr_code').split('/')[-1]
        #print(f"Session ID (from QR URL): {sessionID}")
        
        allowed_origins = ["https://reliable-equatorial-heron.anvil.app"]
        response_headers = {}
        if anvil.server.request.origin in allowed_origins:
            response_headers["Access-Control-Allow-Origin"] = anvil.server.request.origin
            response_headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
            response_headers["Access-Control-Allow-Headers"] = "Content-Type"
            
            formatted_response = {
                "sessionId": sessionId
            }          
            print("Sending to client:", formatted_response)
            
            return anvil.server.HttpResponse(
                200,
                headers=response_headers,
                body=formatted_response
            )
    except Exception as e:
        print(f"Error in create_session: {str(e)}")
        return anvil.server.HttpResponse(500, body={"error": str(e)})

#run this on form show
@anvil.server.callable
def yoti_session():
  print('Hit yoti session')

  yoti_client = Client(YOTI_CLIENT_SDK_ID, YOTI_PRIVATE_KEY_PATH)
  print("Launched Yoti Client")
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
  
    
    # What are we getting back from share_url
    print("Full share_url object:", vars(share_url))
    print("Generated share URL:", share_url.share_url)
    print("Available methods:", dir(share_url))
    
    # Flask app does this so...
    context = {"clientSdkId": YOTI_CLIENT_SDK_ID,"shareUrl": share_url.share_url}
    print(context)
    return context

  #Other SDKs use 
    
    # Or Just return the share_url object to be handled by create_session
    # return share_url.share_url, sessionId
    
  except Exception as e:
    print(f"Error creating share session: {e}")
    

@anvil.server.route("/yoti-callback", methods=["POST"])
def retrieve_profile():
    print("Hit callback")
    try:
      yoti_client = Client(YOTI_CLIENT_SDK_ID, YOTI_PRIVATE_KEY_PATH) #?
      activity_details = yoti_client.get_activity_details(anvil.server.request.body_json.get("token"))
      print(activity_details)
    #   profile = activity_details.profile
    #   profile_dict = vars(profile)

    #   context = profile_dict.get("attributes")  
    #   context["user_id"] = getattr(activity_details, "user_id")
    #   context["parent_remember_me_id"] = getattr(
    #         activity_details, "parent_remember_me_id"
    #     )
    #   context["receipt_id"] = getattr(activity_details, "receipt_id")
    #   context["timestamp"] = getattr(activity_details, "timestamp")
    #   print(f"Token:{token}")
    
    except Exception as e:
       print(f"Error retrieving token: {e}")
    #     # print(f"Error retrieving profile: {e}")
    #     # return anvil.server.HttpResponse(500, body="Error processing callback")







# Ancillary / Revisit

#Source Constraints

# def get(self, request, *args, **kwargs):
#         client = Client(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)
#         constraint = (
#             SourceConstraintBuilder().with_driving_licence().with_passport().build()
#         )
#         policy = (
#             DynamicPolicyBuilder()
#             .with_full_name(constraints=constraint)
#             .with_structured_postal_address(constraints=constraint)
#             .build()
#         )
#         scenario = (
#             DynamicScenarioBuilder()
#             .with_policy(policy)
#             .with_callback_endpoint("/yoti/auth")
#             .build()
#         )
#         share = create_share_url(client, scenario)
#         context = {
#             "yoti_client_sdk_id": YOTI_CLIENT_SDK_ID,
#             "yoti_share_url": share.share_url,
#         }
#         return self.render_to_response(context)