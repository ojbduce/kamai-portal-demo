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
from .Test_Users import existing_users
from .Test_Users import select_user

# 1. CREATE OR A NEW USER OR RECOGNISE AN EXISTING USER 2. LOG-IN THE USER

@anvil.server.callable
def test_user():
  user_data = select_user(existing_weight = 0.3)
  remember_me_id = user_data.get('rememberMeId')
  verification_date = user_data.get('verificationDate')
  email = user_data.get('email')
  existing_user = app_tables.users.search(remember_me_id=remember_me_id)
  if existing_user:
    login_test_user(remember_me_id)
  else:
    try:
        new_user = app_tables.users.add_row(
            remember_me_id=remember_me_id, 
            verification_date= verification_date,
            email=email)
        print("User data received and added to the Users Table.")
        login_test_user(new_user) #this
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

