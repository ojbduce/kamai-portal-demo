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
import secrets

    
#Main Function
@anvil.server.http_endpoint("/yka", methods=["POST"], enable_cors=True)
def receive_user_details():
    print("Hit users endpoint!")
    userData = anvil.server.request.body_json
    print(f"Data Received: {bool(userData)}")  
    print(f"Keys received: {userData.keys()}")  
    print(f"Data dump: {userData}")  
    
    # Check required fields
    if not all(key in userData for key in ['email', 'rememberMeId', 'verificationDate']):
        return {"status": "error", "message": "Missing required fields"}, 400
    
    print("All data available. Adding to the Data Table")
    email = userData['email']
    remember_me_id = userData['rememberMeId']
    verification_date = datetime.now()
    
    # Check if the user already exists
    existing_user = app_tables.users.get(remember_me_id=remember_me_id)
    if existing_user:
        anvil.users.force_login(existing_user)
        print("Existing user logged into App 1.")
        
        # Try logging into the embedded app
        try:
            log_in_embedded_app(remember_me_id)
            print("Existing User logged into Embedded App.")
        except Exception as e:
            print(f"Login to Embedded App failed: {e}")
        
        return {"status": "success", "message": "Existing user logged in"}
    
    else:
        # Create and log in new user
        try:
            new_user = add_user_to_db(email, remember_me_id, verification_date)
            anvil.users.force_login(new_user)
            print("New user logged into App 1.")
            generate_token(remember_me_id)
            
            # Try logging into the embedded app
            try:
                log_in_embedded_app(remember_me_id)
                print("New User logged into Embedded App")
                generate_token(remember_me_id)
            except Exception as e:
                print(f"Login to Embedded App failed: {e}")
        except Exception as e:
            print(f"Error adding new user to the database: {e}")
            return {"status": "error", "message": str(e)}, 500

        return {"status": "success", "message": "User added successfully"}

@anvil.server.callable
def log_in_embedded_app(remember_me_id):
    try:
        print("Hit login embedded app.")
        response = requests.post(
            "https://super-kaleidoscopic-wader.anvil.app/_/api/force-login",  # Ensure the correct endpoint
            json={"remember_me_id": remember_me_id}
        )
        response_data = response.json()
        if response.status_code == 200:
            print("Embedded App login successful:", response_data)
        else:
            print("Embedded App login failed:", response_data)
    except Exception as e:
        print(f"Error logging into Embedded App: {e}")




#Bypass Yoti for testing
@anvil.server.callable
def generate_proxy_user():
  #ADD IP ADDRESS? TBD
  #ADD ERROR HANDLING OR LET MAIN FUNCTION HANDLE?
  from faker import Faker
  fake = Faker()
  email = fake.email()
  remember_me_id = secrets.token_urlsafe(32)
  verification_date = datetime.now()
  return email,remember_me_id,verification_date
#generate_token(remember_me_id)

def add_user_to_db(email,remember_me_id,verification_date):
  print("Adding User to database")
  new_user_row = app_tables.users.add_row(
    email=email,
    remember_me_id=remember_me_id,
    verification_date=verification_date
  )
  return new_user_row

@anvil.server.callable
def generate_token(remember_me_id):
    # from datetime import datetime, timedelta
    # Fetch the user by remember_me_id
    user = app_tables.users.get(remember_me_id=remember_me_id)
    if not user:
        raise Exception("Generate Token: User not found")
    token = 'remember_me_id =' + remember_me_id
    print(f"Token for url hash is: {token}")
    # expires = datetime.now() + timedelta(hours=1)  
    # app_tables.tokens.add_row(
    #     token=token,
    #     user=user,
    #     created=datetime.now(),
    #     expires=expires,
    #     used=False
    # )
    return token
     

@anvil.server.callable
def force_login(user):
    if user:
        anvil.users.force_login(user)
        print(f"User logged in {user['remember_me_id']}")
        return f"Logged in with remember_me_id: {user['remember_me_id'][:6]}..."
    else:
      message = "Force login failed."
      print(message)
      return message

@anvil.server.callable
def test_user_flow():
  email,remember_me_id,verification_date = generate_proxy_user()
  print("Generated Proxy User")
  print(add_user_to_db(email,remember_me_id, verification_date))
  generate_token(remember_me_id)
  force_login(remember_me_id)
  log_in_embedded_app(remember_me_id) # trying Anvil Users does not work.
  return remember_me_id
  
  
  




     
 

















