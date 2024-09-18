from ._anvil_designer import Form1Template
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Check if a user is already logged in
    user = anvil.users.get_user(allow_remembered=True)
    
    if user:
      # User is already logged in
      alert(f"Welcome back, {user['email']}")
     
    else:
      # User is not logged in; prompt login
      self.label_login.text = "Logged-out"
      anvil.users.login_with_form()
    
    self.set_logged_in_user()
    

  def set_logged_in_user(self):
    user = anvil.users.get_user(allow_remembered=True)
    alert("Welcome!")
    self.label_login.text = f"Logged in as {user['email']}"

  