import anvil.secrets
import anvil.files
from anvil.files import data_files
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime, timedelta
import secrets
from .Test_Users import existing_users

import anvil.secrets

FALL_BACK_ID = anvil.secrets("fallback_id")
FALL_BACK_USER = app_tables.users.get(remember_me_id=FALL_BACK_ID)

@anvil.server.callable
def fall_back_user():
  print("Hit fall_back_user server side")
  user = anvil.users.force_login(FALL_BACK_USER)
  print(f"Reverting to fall-back user {user}")
  return anvil.users.get_user(allow_remembered=True)

def force_login(user):
  log_in = anvil.users.force_login(user)
  return anvil.users.get_user(allow_remembered=True)
  
# 1. USER TESTING. CREATE OR A NEW USER OR FAKE AN EXISTING USER 2. LOG-IN THE USER

def generate_new_user():
  from faker import Faker
  fake = Faker()
  return {
        "email": fake.email(),
        "rememberMeId": secrets.token_urlsafe(32),
        "verificationDate": datetime.now()
}

# def select_user(existing_weight=0):
#     if random.random() < existing_weight:
#         return random.choice(existing_users)
#     else:
#         new_user = generate_new_user()
#         existing_users.append(new_user)
#         return new_user

def select_user():
  new_user = generate_new_user()
  print(f"remember_me_id from generate_new_user: {new_user['rememberMeId']}")
  return new_user


@anvil.server.callable
def add_test_user():
  user_data = generate_new_user()
  remember_me_id = user_data.get('rememberMeId')
  print(f"remember_me_id from select_user {remember_me_id}")
  verification_date = user_data.get('verificationDate')
  email = user_data.get('email')
  existing_user = app_tables.users.get(remember_me_id=remember_me_id) #get row here?
    try:
        new_user = app_tables.users.add_row(
            remember_me_id=remember_me_id, 
            verification_date= verification_date,
            email=email)
        print(f"new_user is users table row? {new_user}")
        login_test_user(new_user) #this should be the row 
        return {"status": "success", "message": "User added successfully"}
    except Exception as e:
        print(f"Error adding to Data Table: {e}") 
        return {"status": "error", "message": str(e)}, 500

@anvil.server.callable
def login_test_user(user_row):
    print(f"Hit login with user row {user_row}")
    if user_row is not None:
      anvil.users.force_login(user_row)
      print(f"user: {user_row} is logged-in?")
      return user_row['remember_me_id']
    else:
      print("test_user_login has returned None")
      return None

