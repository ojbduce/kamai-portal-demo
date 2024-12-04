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
        app_tables.users.add_row(
            remember_me_id=remember_me_id, 
            verification_date= verification_date,
            email=email)
        print("User data received and added to the Users Table.")
        login_test_user(remember_me_id) #this
        return {"status": "success", "message": "User added successfully"}
    except Exception as e:
        print(f"Error adding to Data Table: {e}") 
        return {"status": "error", "message": str(e)}, 500

@anvil.server.callable
def login_test_user(remember_me_id):
    print(f"Hit login with ID {remember_me_id}")
    user = app_tables.users.get(remember_me_id=remember_me_id)
    print(f"func login_test_user: user = {user}")
    if user is not None:
      anvil.users.force_login(user)
      print(f"user: {remember_me_id} is logged-in")
      return user['remember_me_id']
    else:
      print("test_user_login has returned None")
      return None

