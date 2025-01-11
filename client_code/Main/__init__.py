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
    self.remember_me_id = ''
    self.yoti_loggin_in_box.visible = False #MOVE UI SET UP TO OWN METHOD?
    self.button_show_data.visible = False
    # anvil.server.call('hello')
    anvil.js.window.console.log("Kaimai Home Page. Logging in User")
    try:
      anvil.js.window.console.log("Logging In USER")
      print("Logging in User")
      user = anvil.users.get_user(allow_remembered=True) #we want to be using the Usets Service expliticitly.
      if user:
        anvil.js.window.console.log("Client has found Existing User")
        print(f"Client has found Existing user {user['remember_me_id']}")
        self.remember_me_id = user['remember_me_id']
        print("self.remember_me_id variable is set")
        self.show_yoti_logged_in_box()
        anvil.server.call('log_in_embedded_app', self.remember_me_id)
      else:
        print("No Yoti User found")
      # self.show_yoti_logged_in_box()
      if user is None:
        print("Hit if user is None") #OK
        #Slightly redundant this fallback as we have a synthetic loin button option from QR_login
        #user = anvil.server.call('fall_back_user') # won't call so try separate func
        self.use_fallback_user()#was fine now doesn't call
        anvil.js.window.console.log("Fallback User")
        user = anvil.users.get_user(allow_remembered=True)
        if user:
          print(f" User logged-in: {user['email']}")
          self.remember_me_id = user['remember_me_id']
          print('self.remember_me_id is set')
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

  def link_digi_leaders_image_click(self, **event_args):
      """This method is called when the link is clicked"""
      # url = 'https://adept-right-category.anvil.app' #users does not work
      # self.link_digi_leaders_image.url =url
      url = 'https://super-kaleidoscopic-wader.anvil.app/#!?remember_me_id=' + self.remember_me_id
      print(f"URL is {url}")
      self.link_digi_leaders_image.url =url
    
      
  def show_yoti_logged_in_box(self):
    print("Hit show_yoti_login func")
    self.yoti_loggin_in_box.visible = True
    self.yoti_loggin_in_box.tooltip = "Logged in with Yoti"
    self.button_show_data.visible = True

  def get_data(self):
    rows = app_tables.reports.search()
    self.repeating_panel_1.items = rows
    #print(rows)# Bind rows to the Repeating Panel
    
      
  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.get_data()
    self.outlined_card_digi_leaders.visible = False
    self.card_database.visible = True
    self.label_title.visible = False

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('header')

  # def url_test_button_click(self, **event_args):
  #   """This method is called when the button is clicked"""
  #   share_url = anvil.server.call('yoti_session')
  #   self.label_return_message.visible = True
  #   self.label_return_message.text = share_url
  #   if share_url == "Keys not found":
  #     Notification("Keys not found")
  #   elif share_url == "Error creating share session.":
  #     Notification("Error creating share session.")
  #   else:
  #     Notification("Share_Url test passed")
    

  # def button_test_bd_click(self, **event_args):
  #   """This method is called when the button is clicked"""
  #   self.name = 'test_444'
  #   app_tables.files.add_row(name = self.name)
  #   print("Added file to files table")
  #   for row in app_tables.files.search():
  #     print(row['name'])

 

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert("Next...")

  # def link_2_copy_click(self, **event_args):
  #   """This method is called when the link is clicked"""
  #   pass

  def button_show_data_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.get_data()
    self.outlined_card_digi_leaders.visible = False
    self.card_database.visible = True
    self.label_title.visible = False

  def button_about_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  


 # def button_1_click(self, **event_args):
  #   """This method is called when the button is clicked"""
  #   anvil.server.call('check_origin')

  # def button_server_session_test_click(self, **event_args):
  #   """This method is called when the button is clicked"""
  #   anvil.server.call('server_session_data')

  # def button_cookies_click(self, **event_args):
  #   anvil.server.call('cookies')
  #   anvil.server.call('server_session_data')
  #   """This method is called when the button is clicked"""

  
    
    


    
 
    




  
 