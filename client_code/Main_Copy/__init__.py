from ._anvil_designer import Main_CopyTemplate
from anvil import *
import anvil.server
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
    self.user = self.get_user() #does force_login work?
    print(f"get_user gives: {self.user}")
    print(f"get_user: This user has logged in: {anvil.users.get_user()['remember_me_id']}")
    self.label_logged_in.text = "Awaiting Auto-log-in..."
    self.set_logged_in_user()
    self.content_panel_home.visible = True
    self.card_database.visible = False
    self.flow_panel_title.visible = False

  def set_logged_in_user(self):
    #user = anvil.users.get_user(allow_remembered=True) COME BACK TO THIS
    #self.label_logged_in.text = f"Logged in as {user['remember_me_id']}"
    self.user = self.user
    if self.user:
      self.label_logged_in.text = f"Logged in as {self.user}"
    else:
      print("Set Logged in user label has failed")

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.get_data()
    self.content_panel_home.visible = False
    self.card_database.visible = True

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('header')

  def url_test_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    share_url = anvil.server.call('yoti_session')
    self.label_return_message.visible = True
    self.label_return_message.text = share_url
    if share_url == "Keys not found":
      Notification("Keys not found")
    elif share_url == "Error creating share session.":
      Notification("Error creating share session.")
    else:
      Notification("Share_Url test passed")
    

  def button_test_bd_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.name = 'test_444'
    app_tables.files.add_row(name = self.name)
    print("Added file to files table")
    for row in app_tables.files.search():
      print(row['name'])

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('check_origin')

  def button_server_session_test_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('server_session_data')

  def button_cookies_click(self, **event_args):
    anvil.server.call('cookies')
    anvil.server.call('server_session_data')
    """This method is called when the button is clicked"""
    

  





  
 