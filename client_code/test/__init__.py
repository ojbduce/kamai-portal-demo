from ._anvil_designer import testTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class test(testTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.html = self.column_panel_1
    self.html.content = '''
    hello
    <h1> Hello </h1>'''

    # Any code you write here will run before the form opens.
