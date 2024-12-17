from ._anvil_designer import Yoti_QR_LoginTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
import anvil.js
from anvil.tables import app_tables
from anvil.js.window import jQuery
from anvil.js import get_dom_node



class Yoti_QR_Login(Yoti_QR_LoginTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    anvil.js.window.addEventListener('message', lambda event: self.handle_auth_message(event))
    # iframe = jQuery("<iframe width='100%' height='450px'>").attr("src",'https://kaimaiyoti.azurewebsites.net')
    # iframe.appendTo(get_dom_node(self.iframe_container))
    self.outlined_card.role = 'mid-card'
    self.button_login_test_user.visible = False
    self.button_home.visible = False
    self.cleanup_duplicate_ids()

  def handle_auth_message(self, event):
    if event.data == 'auth_success':
      anvil.open_form('Home')

    
  def cleanup_duplicate_ids(self):#why doesn't work??
    duplicates = set()
    duplicate_count = 0
    for row in app_tables.users.search():
      remember_me_id = row['remember_me_id']
      print(remember_me_id)
    if remember_me_id in duplicates:
      row.delete()
      duplicate_count +=1
    else:
      duplicates.add(remember_me_id)
      print(len(duplicates))
      print(f"{duplicate_count}rows removed") #0 
      

  def button_show_tests_click(self, **event_args):
    self.button_login_test_user.visible = True
    self.button_home.visible = True
    self.button_show_tests.visible = False

  def label_loading_show(self, **event_args):
    """This method is called when the Label is shown on the screen"""
    self.label_loading.text = "Your Yoti QR Code is loading..."
    time.sleep(5)
    self.label_loading.visible = False

  def button_home_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Home')

  def button_login_test_user_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.server.call('test_user')
    return user , open_form('Home')
