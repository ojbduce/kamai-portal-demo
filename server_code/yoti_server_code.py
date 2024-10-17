import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from yoti_python_sdk.client import Client

YOTI_CLIENT_SDK_ID = 'your_sdk_id'
YOTI_PRIVATE_KEY_PATH = '_/theme/keys/Yoti-For-Kaimai-access-security.pem'
yoti_client = Client(YOTI_CLIENT_SDK_ID, YOTI_PRIVATE_KEY_PATH)

