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
    self.label_return_message.visible = False
    self.outlined_card_testing.visible = False
    self.modal_qr_button.visible = False
    self.journals.visible = False

    
    # Check if a user is already logged in
    #user = anvil.users.get_user(allow_remembered=True)
   
    # if user:
    #   # User is already logged in
    #    self.set_logged_in_user()

    # else:
    #   # User is not logged in; prompt login
    #   self.label_login.text = "Logged-out"
    #   anvil.users.login_with_form()
    self.content_panel_home.visible = True
    self.card_database.visible = False
    
   
  def handle_click(self, **event_args):
    alert("The button got clicked!")
    
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


  def check_box_test_card_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.check_box_test_card.checked = self.outlined_card_testing.visible
    # self.check_box_test_card.checked = self.outlined_card_testing.visible = not self.check_box_test_card.checked

  def button_test_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.outlined_card_testing.visible = True

  def yoti_button_click(self, param, **event_args):
    """This method is called click"""
    alert('click')

  def outlined_button_login_register_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.modal_qr_button.visible = True

      

    






  
 