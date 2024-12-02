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

@anvil.server.callable
def server_session_data():
  print (type(anvil.server.session))
  #<class 'anvil._threaded_server.LocalCallInfo'>
  print(anvil.server.session)  # Print all session data
  print(dir(anvil.server.session))  # Check available methods and attributes
 

@anvil.server.callable
def cookies():
  print (type(anvil.server.cookies.local))
  print("Printing Cookies")
  print(anvil.server.cookies.local)
  print(anvil.server.cookies.shared)
  #<class 'anvil._server.AnvilCookie'>
  #for key, value in anvil.server.session.cookies.local.items():
    #print(f"Local Cookies: {key}: {value}")
  #for key, value in anvil.server.session.cookies.shared.items():
  #print(f"Shared Cookies: [key]:{value}")
  anvil.server.cookies.local.
 

