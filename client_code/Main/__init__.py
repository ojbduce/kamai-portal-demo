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
# import time


class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form pfrom ._anvil_designer import MainTemplate
    self.init_components(**properties)
    self.yoti_loggin_in_box.visible = False
    # self.button_show_data.visible = False
    # anvil.server.call('hello')
    # TO DO: FUNCTION: GET USER FROM HASH URL PARAMETERS 
    #Login with Yoti remember_me_id. Fallback to default or Login with form.
    anvil.js.window.console.log("Kaimai Home Page. Logging in User")
    try:
      user = anvil.users.get_user(allow_remembered=True) #we want to be using the Usets Service expliticitly.
      print(f"Client has found user {user['email']}") 
      self.show_yoti_logged_in_box()
      if user is None:
        print("Hit if user is None") #OK
        # anvil.server.call('hello')
        self.use_fallback_user()#won't call
        #user = anvil.server.call('fall_back_user') # won't call
        anvil.js.window.console.log("Enrolling Guest User")
        print(f"Reverting to default user {user['remember_me_id']}")
        user = anvil.users.get_user(allow_remembered=True)
        if user:
          print(f" User logged-in: {user['email']}")
          self.show_yoti_logged_in_box()
      else:
        anvil.js.window.console.log("Reverting to Login Form")
        anvil.users.login_with_form(allow_remembered=True)
    except Exception as e:
      anvil.js.window.console.log("Error anvil,users.get_user generating {e} null type.User not found Client side")
    self.outlined_card_digi_leaders.visible = True
    self.card_database.visible = False 
    self.label_title.visible = True

  def use_fallback_user(self):
    print("Hit fallback user func")
    user = anvil.server.call('fall_back_user')
    return user
    
  def show_yoti_logged_in_box(self):
    print("Hit show_yoti_login func")
    time.sleep = 1
    self.yoti_loggin_in_box.visible = True
    self.yoti_loggin_in_box.tooltip = "Logged in with Yoti"
    # self.button_show_data.visible = True
    
      
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
    self.get_data()
    self.outlined_card_digi_leaders.visible = False
    self.card_database.visible = True
    self.label_title.visible = False

  def button_show_data_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.get_data()
    self.outlined_card_digi_leaders.visible = False
    self.card_database.visible = True
    self.label_title.visible = False


    
 
    




  
 