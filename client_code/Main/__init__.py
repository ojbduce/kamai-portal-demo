from ._anvil_designer import MainTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users


class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form pfrom ._anvil_designer import MainTemplate
    self.init_components(**properties)
    user = anvil.users.get_user(allow_remembered=True)
    # user = anvil.users.force_login()
    # user = anvil.users.get_user()['remember_me_id'] #is None type
    if user:
      print("Client:init: Anvil Users Service row object = {user} ")
      # self.label_logged_in.text = f"User: {anvil.users.get_user()['remember_me_id']}"
      self.label_logged_in.text = f"User: {user}"
    else:
      print("User not found Client-side")
      self.label_logged_in.text = "Waiting for Yoti log-in"
    # if user and 'remember_me_id' in user:
    #   self.label_logged_in.text = f"User: {anvil.users.get_user()['remember_me_id']}"
    # else:
    #   self.label_logged_in.text = "Waiting for Yoti log-in"
    #self.label_logged_in.text = "Awaiting Auto-log-in..."
    self.outlined_card_digi_leaders.visible = True
    self.card_database.visible = False 
    self.label_title.visible = True
    
  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.get_data()
    self.outlined_card_digi_leaders.visible = False
    self.card_database.visible = True
    self.label_title.visible = False

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

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert("Next...")

  def link_2_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
    

  





  
 