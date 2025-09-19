from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import LinearPanel, Slot, WithLayout, Button


class Form2(Form2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

class MyLayout(LinearPanel):
  def __init__(self, **properties):
    super().__init__(**properties)
    header_slot = Slot(self, 0, {})
    content_slot = Slot(self, 1, {})
    self.slots = {"header": header_slot, "content": content_slot}

class Page(WithLayout, layout=MyLayout):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.layout.slots["header"].add_component(Button(text="Back"))
    self.layout.slots["content"].add_component(Button(text="Do Thing"))

    # Any code you write here will run before the form opens.
