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
    user_rows = app_tables.users.search(tables.order_by('last_login',ascending = True))
    self.repeating_panel_2.items = user_rows
    report_rows = app_tables.reports.search()
    self.repeating_panel_reports.items = report_rows

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Home')

  def button_about_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
    
    