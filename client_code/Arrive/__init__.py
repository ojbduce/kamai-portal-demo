from ._anvil_designer import ArriveTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Modal_Login_Prompt import Modal_Login_Prompt
from ..Yoti_QR_Login import Yoti_QR_Login


class Arrive(ArriveTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    # modal_link = Modal_Login_Prompt()
    # alert(content = modal_link, buttons=[] )
    modal_login_page = Yoti_QR_Login()
    alert(content = modal_login_page, large=True,buttons=[])
    
    
