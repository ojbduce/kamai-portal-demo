from ._anvil_designer import Yoti_QR_Login_AltTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
import anvil.js
from anvil.tables import app_tables
from anvil.js.window import jQuery
from anvil.js import get_dom_node


class Yoti_QR_Login_Alt(Yoti_QR_Login_AltTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    anvil.js.window.addEventListener(
      "message", lambda event: self.handle_auth_message(event)
    )
    # iframe = jQuery("<iframe width='100%' height='450px'>").attr("src",'https://kaimaiyoti.azurewebsites.net')
    # iframe.appendTo(get_dom_node(self.iframe_container))
    self.outlined_card.role = "mid-card"

  def handle_auth_message(self, event):
    print("\n=== Message Inspection ===")
    print("1. Raw data:", event.data)
    print("2. Type:", type(event.data))

    # For proxy objects (like system messages)
    if hasattr(event.data, "keys"):
      keys = list(event.data.keys())
      print("3. Available keys:", keys)

      if "fn" in keys:
        print(f"System message: {event.data['fn']}")
        return  # Skip system messages

    # For our auth message (should be a string)
    if isinstance(event.data, str):
      if event.data.startswith("auth_success:"):
        _, remember_me_id = event.data.split(":", 1)
        print(f"Got remember_me_id: {remember_me_id}")
        user = app_tables.users.get(remember_me_id=remember_me_id)
        print(f"Identified User from handle_auth: {user['email']}")
        anvil.server.call("force_login", user)  # force login only server-side
        print(f"handle_auth has force logged in user:{user['email']}")
        anvil.open_form("Home")
        return

    print("Unhandled message type or format")

    # print("Raw event data:", event.data)
    # anvil.js.window.console.log("Raw event data:", event.data)
    # if isinstance(event.data, str):
    #   if event.data.startswith('auth_success:'):
    #     # Split the string to get the remember_me_id
    #     _, remember_me_id = event.data.split(':', 1)  # Use maxsplit=1
    #     print(f"Got remember_me_id: {remember_me_id}")
    #     anvil.js.window.console.log(f"Got remember_me_id: {remember_me_id}")
    #     anvil.open_form('Home')
    #   elif event.data == 'auth_success':
    #     print("Got simple auth_success message")
    #     anvil.open_form('Home')
    # else:
    #   print(f"Got unexpected data type: {type(event.data)}")
    #   anvil.js.window.console.log(f"Unexpected message type: {type(event.data)}")

    # if event.data == 'auth_success':
    # user = anvil.users.get_user(allow_remembered=True)
    # print(user)
    # print("Yoti Login: Hit handle_auth")
    # anvil.js.window.console.log("Yoti Login: Hit handle_auth")

    # data = event.data
    # if data:
    #   anvil.js.window.console.log("Data")
    #   if isinstance(data, dict) and data.get('type') == 'auth_success':
    #       print("data,dict auth_success")
    #       anvil.js.window.console.log("data,dict auth_success")
    #       remember_me_id = data.get('remember_me_id')
    #       # remember_me_id = unquote(unquote(remember_me_id))
    #       print(f"Decoded remember_me_id: {remember_me_id}")
    #       print(remember_me_id)
    #       anvil.js.window.console.log(remember_me_id)
    #       anvil.open_form('Home')
    #   elif event.data == 'auth_success':
    #     print("Just auth success")
    #     anvil.js.window.console.log("Just auth")
    #     anvil.open_form('Home')
    #   elif event.data == 'auth_success':
    #     print("Just auth success. Trying Main")
    #     anvil.js.window.console.log("Just auth Trying Main")
    #     anvil.open_form('Main')
    # else:
    #   print("Error")
    #   anvil.js.window.console.log("Error")
    #   anvil.open_form('Home')

    # Construct URL with remember_me_id
    # if event.data == 'auth_success':
    #

  def cleanup_duplicate_ids(self):  # why doesn't work??
    duplicates = set()
    duplicate_count = 0
    for row in app_tables.users.search():
      remember_me_id = row["remember_me_id"]
      print(remember_me_id)
    if remember_me_id in duplicates:
      row.delete()
      duplicate_count += 1
    else:
      duplicates.add(remember_me_id)
      print(len(duplicates))
      print(f"{duplicate_count}rows removed")  # 0

  # Now redundant?
  def label_loading_show(self, **event_args):
    """This method is called when the Label is shown on the screen"""
    self.label_loading.text = "Your Yoti QR Code is loading..."
    time.sleep(5)
    self.label_loading.visible = False

  ##Does this work with Users Service? Add url hash? Add Existing user version.
  def button_login_test_user_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.server.call("test_user_flow")
    print(f"Test User remember_me_id is: {user}")
    print(anvil.users.get_user(allow_remembered=True))
    return user, open_form("Main")
