from ._anvil_designer import Data_ViewTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users


class Data_View(Data_ViewTemplate):
  def __init__(self, **properties):
    # Set Form pfrom ._anvil_designer import MainTemplate
    self.init_components(**properties)
    