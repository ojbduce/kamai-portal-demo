from ._anvil_designer import Arrive_devTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.js
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js import get_dom_node
from ..Modal_Login_Prompt import Modal_Login_Prompt
from ..Yoti_QR_Login import Yoti_QR_Login


class Arrive_dev(Arrive_devTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Authentication instance variables
    try:
      print("Using fall back user")
      user, self.remember_me_id = anvil.server.call('fall_back_user')
      print('remember_me_id')
      print(f"fallback_id {user['remember_me_id']}")
      anvil.js.window.console.log("Fallback User")
      print(user)
      if user:
        print(f" User logged-in: {user['email']}")
        self.remember_me_id = user['remember_me_id']
        self.is_authenticated = True
        print('self.remember_me_id is set')
        self.show_yoti_logged_in_status()
      else:
        anvil.js.window.console.log("Reverting to Login Form")
        anvil.users.login_with_form(allow_remembered=True)
    except Exception as e:
      anvil.js.window.console.log("Error anvil,users.get_user generating {e} null type.User not found Client side")
    except Exception as e:
      anvil.js.window.console.log("Error anvil,users.get_user generating {e} null type.User not found Client side")

  def show_yoti_logged_in_status(self):
    """Update UI to show logged in status"""
    try:
      # Update admin button visibility
      if self.is_authenticated:
        self.dom_nodes['admin-btn'].style.display = 'block'
        self.dom_nodes['login-btn'].style.display = 'none'
        # Add login indicator
        login_indicator = self.dom_nodes['login-status']
        if login_indicator:
          login_indicator.textContent = "Logged in with Yoti"
          login_indicator.style.display = 'block'
      else:
        self.dom_nodes['admin-btn'].style.display = 'none'
        self.dom_nodes['login-btn'].style.display = 'block'
    except Exception as e:
      print(f"UI update error: {e}")

  def home_click(self, **event_args):
    """Navigate to Home form with authentication state"""
    if self.is_authenticated:
      open_form('Main', remember_me_id=self.remember_me_id)
    else:
      open_form('Main')

  def admin_click(self, **event_args):
    """Navigate to Admin form if authenticated"""
    if self.is_authenticated:
      open_form('Admin', remember_me_id=self.remember_me_id)
    else:
      self.login_click()

  def about_click(self, **event_args):
    """Navigate to About form"""
    # Create an about form or show info
    alert("About Kaimai Directory\n\nA proof of concept authentication directory using Yoti integration.")

  def login_click(self, **event_args):
    """Show login modal"""
    modal_login_page = Yoti_QR_Login()
    alert(content=modal_login_page, large=True, buttons=[])

  def openForm(self, title=None, **kwargs):
    """This method is called when a visit button is clicked"""
    # Map publication titles to Anvil forms
    form_mapping = {
      'Digital Leaders': 'Main',  # Updated to pass through Main for auth
      'Science Today': 'Main',
      'The Culinary Chronicle': 'Main',
      'Global Affairs': 'Main',
      'Digital Marketing Trends': 'Main',
      'Historical Studies Quarterly': 'Main',
      'Architectural Digest': 'Main',
      'Health & Wellness Journal': 'Main',
      'Breaking News Network': 'Main',
      'Travel Enthusiast': 'Main',
      'Economic Review': 'Main'
    }

    # Get the form name from the mapping, default to 'Main'
    form_name = form_mapping.get(title, 'Main')

    # Open the appropriate form with authentication state
    if self.is_authenticated:
      open_form(form_name, remember_me_id=self.remember_me_id, publication_title=title)
    else:
      # Prompt for login first
      self.login_click()
