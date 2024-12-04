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


# Select User

# Add User To Database - this calls Select User
def login_synthetic_test(remember_me_id,verification_date,email):
  select_user = select_user(existing_weight = 0.3)
  existing_user = app_tables.users.search(remember_me_id=remember_me_id)
  if existing_user:
    login_with_synth_id(remember_me_id)
  else:
    try:
        app_tables.users.add_row(
            remember_me_id=remember_me_id, 
            verification_date= verification_date,
            email=email)
        print("User data received and added to the Users Table.")
        login_with_synth_id() #this
        return {"status": "success", "message": "User added successfully"}
    except Exception as e:
        print(f"Error adding to Data Table: {e}") 
        return {"status": "error", "message": str(e)}, 500

@anvil.server.callable
def login_with_synth_id(remember_me_id):
    print("Hit login with ID")
    user = app_tables.users.get(remember_me_id=remember_me_id)
    if user is not None:
      anvil.users.force_login(user)
      print(f"user: {remember_me_id} is logged-in")
      return user['remember_me_id']
    else:
      return None

