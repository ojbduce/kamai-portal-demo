from ._anvil_designer import Main_CopyTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users


class Main_Copy(Main_CopyTemplate):
  def __init__(self, **properties):
    # Set Form pfrom ._anvil_designer import MainTemplate
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

    self.content_panel_home.visible = True
    self.card_database.visible = False

    self.get_data()

  def get_data(self):
    rows = app_tables.reports.search()
    self.repeating_panel_1.items = rows
    #print(rows)# Bind rows to the Repeating Panel
   

  def set_logged_in_user(self):
    user = anvil.users.get_user(allow_remembered=True)
    self.label_login.text = f"Logged in as {user['email']}"

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.get_data()
    self.content_panel_home.visible = False
    self.card_database.visible = True

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('header')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert("Coming soon!")


  
 