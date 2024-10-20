from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if self.item:
            self.label_email.text = self.item.get('email', 'No email')
            self.label_report.text = self.item.get('report', 'No report')
    

    # Any code you write here will run before the form opens.
