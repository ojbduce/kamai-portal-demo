import anvil.files
from anvil.files import data_files
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
@anvil.server.callable
def server_session_data():
  print (type(anvil.server.session))
  #<class 'anvil._threaded_server.LocalCallInfo'>
  for key, value in anvil.server.session.items():
        print(f"{key}: {value}")

@anvil.server.callable
def cookies():
  print (type(anvil.server.cookies.local))
  #<class 'anvil._server.AnvilCookie'>
  for key, value in anvil.server.session.cookies.local.items():
    print(f"Local Cookies: {key}: {value}")
  for key, value in anvil.server.session.cookies.shared.items():
    print(f"Shared Cookies: [key]:{value}")
 

