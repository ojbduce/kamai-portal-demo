from ._anvil_designer import Yoti_QR_LoginTemplate
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
import time


class Yoti_QR_Login(Yoti_QR_LoginTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    iframe = jQuery("<iframe width='100%' height='600px'>").attr("src",'https://kaimaiyoti.azurewebsites.net')
    iframe.appendTo(get_dom_node(self.column_panel_iframe))
    self.button_login_test_user.visible = False
    self.button_home.visible = False
    self.label_loading.visible = True
    

    # Any code you write here will run before the form opens.

  def button_show_tests_click(self, **event_args):
    self.button_login_test_user.visible = True
    self.button_home.visible = True
    self.button_show_tests.visible = False

  def label_loading_show(self, **event_args):
    """This method is called when the Label is shown on the screen"""
    self.label_loading.text = "Your Yoti QR Code is loading..."
    time.sleep(5)
    self.label_loading.visible = False

  def button_home_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Home')

  def button_login_test_user_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.server.call('test_user')
    return user , open_form('Home')
