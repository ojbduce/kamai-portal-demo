from ._anvil_designer import Yoti_ButtonTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js


class Yoti_Button(Yoti_ButtonTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    
   