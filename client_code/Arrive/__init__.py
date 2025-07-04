from ._anvil_designer import ArriveTemplate
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
from ..Modal_Login_Prompt import Modal_Login_Prompt
from ..Yoti_QR_Login import Yoti_QR_Login


class Arrive(ArriveTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # anvil.js.get_dom_node()

    # Any code you write here will run before the form opens.

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    # modal_link = Modal_Login_Prompt()
    # alert(content = modal_link, buttons=[] )
    modal_login_page = Yoti_QR_Login()
    alert(content = modal_login_page, large=True,buttons=[])

  def openForm(self, title=None, **kwargs):
    """This method is called when a visit button is clicked"""
    alert("Clicked")
    
    form_mapping = {
      'Digital Leaders': 'Home',  # You can change this to any available form
    #   'Science Today': 'Home',
    #   'The Culinary Chronicle': 'Home',
    #   'Global Affairs': 'Home',
    #   'Digital Marketing Trends': 'Home',
    #   'Historical Studies Quarterly': 'Home',
    #   'Architectural Digest': 'Home',
    #   'Health & Wellness Journal': 'Home',
    #   'Breaking News Network': 'Home',
    #   'Travel Enthusiast': 'Home',
    #   'Economic Review': 'Home'
    }

    # # Get the form name from the mapping, default to 'Home'
    form_to_open = form_mapping.get(title, 'Home')

    # # Open the appropriate form
    open_form(form_to_open)