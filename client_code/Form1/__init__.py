from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # inside __init__
    self.home_btn = Button(text="Home")
    # self.admin_btn = Button(text="Admin")
    # self.about_btn = Button(text="About")
    # self.login_btn = Button(text="Login")
    # self.login_status_lbl = Label(text="Not logged in", visible=False, role="caption")
    
    self.add_component(self.home_btn) 
    # self.add_component(self.admin_btn, slot='admin_btn_slot')
    # self.add_component(self.about_btn, slot='about_btn_slot')
    # self.add_component(self.login_btn, slot='login_btn_slot')
    # self.add_component(self.login_status_lbl, slot='login_status_slot')
    
    self.home_btn.set_event_handler('click', self.home_click)
    # self.admin_btn.set_event_handler('click', self.admin_click)
    # self.about_btn.set_event_handler('click', self.about_click)
    # self.login_btn.set_event_handler('click', self.login_click)
    
        # Any code you write here will run before the form opens.
