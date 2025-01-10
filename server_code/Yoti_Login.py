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
        print("Existing user logged in")
        return {"status": "success", "message": "Existing user logged in"}
      except Exception as e:
        print(f"login_yoti_failed {e}")
        return {"status": "error", "message": str(e)}, 500
    else:
      try:
        add_user_to_db(email,remember_me_id,verification_date)
        login_yoti(remember_me_id,verification_date,email)
        print("New user logged in")
        return {"status": "success", "message": "User added successfully"} # continue in demo mode!
      except Exception as e:
          print(f"Error adding to Data Table: {e}") 
          return {"status": "error", "message": str(e)}, 500

#login_yoti - Main Function
'''Part of the external verification pipeline. 
Takes an id received from the api. Not called Client-sde, atm'''
@anvil.server.callable
def login_yoti(remember_me_id,verification_date, email):
    print(f"Hit login with ID{remember_me_id}")
    #check for existing user
    user = app_tables.users.get(remember_me_id=remember_me_id)
    #system_password = anvil.secrets.get_secret('system_password')
    if user:
      anvil.users.force_login(user)
      #ADD API LOGIN TO SECOND SITE FUNCTION CALL
    #logging remove later
      print(f"Anvil Users actual user/id check: {anvil.users.get_user()['remember_me_id']}")#OK
      print(f"Existing Yoti User {remember_me_id} is logged-in")#OK
      anvil.server.session['remember_me_id'] = remember_me_id # as Users not working Client-side
      print(f"login_yoti. Server-side success - remember_me_id from server session {anvil.server.session}")
      user = app_tables.users.get(remember_me_id=remember_me_id)
      return user #OR RETURN anvil.users.get_user()? TBD / TEST
      #else fallback / create user for demo purpposes
    else:
      generate_proxy_user()
      print("Generated proxy user")
      add_user_to_db(email,remember_me_id,verification_date)
      print("Added proxy user to db")
      force_login(remember_me_id)
      print(f"Logged in proxy_use {remember_me_id}")
      return user #OR RETURN anvil.users.get_user()? TBD/TEST

@anvil.server.callable
def log_in_embedded_app(remember_me_id):
  try:
          response = requests.post
              "https://app3.anvil.app/_/api/force-login",
              json={"remember_me_id": remember_me_id}
          )
          response_data = response.json()
          if response.status_code == 200:
              print("App 3 login successful:", response_data)
          else:
              print("App 3 login failed:", response_data)
  except Exception as e:
      print(f"Error calling App 3 force-login API: {e}")
      
      return user

@anvil.server.callable
def generate_proxy_user():
  #ADD IP ADDRESS? TBD
  #ADD ERROR HANDLING OR LET MAIN FUNCTION HANDLE?
  from faker import Faker
  fake = Faker()
  return {
        "email": fake.email(),
        "remember_me_id": secrets.token_urlsafe(32),
        "verification_date": datetime.now()
} #OR SHOULD WE RETURN A USER OBJECT AS VARIABLE USER?


def add_user_to_db(email,remember_me_id,verification_date):
  new_user_row = app_tables.users.add_row(
    email=email,
    remember_me_id=remember_me_id,
    verification_date=verification_date
  )
  return new_user_row

@anvil.server.callable
def force_login(remember_me_id):
    user = app_tables.users.get(remember_me_id=remember_me_id)
    if user:
        anvil.users.force_login(user)
        print(f"User logged in {remember_me_id}")
        return remember_me_id
    else:
      print("Force login failed.")
  




     
 

















