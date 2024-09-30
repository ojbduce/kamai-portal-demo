from ._anvil_designer import MainTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users


class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Check if a user is already logged in
    user = anvil.users.get_user(allow_remembered=True)

    if user:
      # User is already logged in
       self.set_logged_in_user()

    else:
      # User is not logged in; prompt login
      self.label_login.text = "Logged-out"
      anvil.users.login_with_form()

   

  def set_logged_in_user(self):
    user = anvil.users.get_user(allow_remembered=True)
    self.label_login.text = f"Logged in as {user['email']}"

  