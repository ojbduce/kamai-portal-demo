from ._anvil_designer import iframe_containerTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import jQuery
from anvil.js import get_dom_node



class iframe_container(iframe_containerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    iframe = jQuery("<iframe width='100%' height='1000 px' outline = none border = none >").attr("src",'https://kaimaiyoti.azurewebsites.net')
    iframe.appendTo(get_dom_node(self))

    # Any code you write here will run before the form opens.
