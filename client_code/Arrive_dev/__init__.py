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

    # Instance state
    self.is_authenticated = False
    self.remember_me_id = ''

    # Bind header events from custom HTML
    self._bind_header_events()

    # Layered authentication flow (per flow.md and Main)
    anvil.js.window.console.log("Arrive: Starting auth checks")
    try:
      user = anvil.users.get_user(allow_remembered=True)
      if user:
        anvil.js.window.console.log("Arrive: Found existing Anvil user")
        print(f"Existing user {user['remember_me_id']}")
        self.remember_me_id = user['remember_me_id']
        self.is_authenticated = True
        self.show_yoti_logged_in_status()
      else:
        print("Arrive: No Anvil Users Service user found")

      # If still not authenticated, try URL hash fallback
      if not self.is_authenticated:
        try:
          print("Arrive: Trying URL hash fallback")
          hash_val = get_url_hash()
          if hash_val:
            self.remember_me_id = hash_val
            print(f"remember_me_id from URL hash: {self.remember_me_id}")
            user = app_tables.users.get(remember_me_id=self.remember_me_id)
            if user:
              logged_in = anvil.server.call('force_login', user)
              print(logged_in)
              self.is_authenticated = True
              self.show_yoti_logged_in_status()
        except Exception as e:
          anvil.js.window.console.log("Arrive URL-hash fallback error {e}")

      # If still not authenticated, try server fallback user (testing)
      if not self.is_authenticated:
        try:
          print("Arrive: Using fallback user")
          user, self.remember_me_id = anvil.server.call('fall_back_user')
          if user:
            print(f"Fallback user: {user['email']}")
            self.remember_me_id = user['remember_me_id']
            self.is_authenticated = True
            self.show_yoti_logged_in_status()
          else:
            anvil.js.window.console.log("Arrive: No fallback user. Showing login form")
            anvil.users.login_with_form(allow_remembered=True)
        except Exception as e:
          anvil.js.window.console.log("Arrive fallback user error {e}")
    except Exception as e:
      anvil.js.window.console.log("Arrive auth error {e}")

  def show_yoti_logged_in_status(self):
    """Update UI to show logged in status"""
    try:
      nodes = self.dom_nodes
      # Update admin and login button visibility
      if 'admin-btn' in nodes:
        nodes['admin-btn'].style.display = 'block' if self.is_authenticated else 'none'
      if 'login-btn' in nodes:
        nodes['login-btn'].style.display = 'none' if self.is_authenticated else 'block'
      # Update login indicator text
      if 'login-status' in nodes and self.is_authenticated:
        nodes['login-status'].textContent = "Logged in with Yoti"
        nodes['login-status'].style.display = 'block'
    except Exception as e:
      print(f"UI update error: {e}")

  def _bind_header_events(self):
    """Bind click handlers to custom HTML header buttons."""
    try:
      nodes = self.dom_nodes
      if 'home-btn' in nodes:
        anvil.js.bind_dom_event(nodes['home-btn'], 'click', lambda evt: self.home_click())
      if 'admin-btn' in nodes:
        anvil.js.bind_dom_event(nodes['admin-btn'], 'click', lambda evt: self.admin_click())
      if 'about-btn' in nodes:
        anvil.js.bind_dom_event(nodes['about-btn'], 'click', lambda evt: self.about_click())
      if 'login-btn' in nodes:
        anvil.js.bind_dom_event(nodes['login-btn'], 'click', lambda evt: self.login_click())
    except Exception as e:
      print(f"Header binding error: {e}")

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

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    # modal_link = Modal_Login_Prompt()
    # alert(content = modal_link, buttons=[] )
    modal_login_page = Yoti_QR_Login()
    alert(content = modal_login_page, large=True,buttons=[])
