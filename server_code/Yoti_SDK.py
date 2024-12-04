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

''' YOTI SDK currently not up to date for Python. So, we have done it in JS,and may come back to Python later. 
For now commented out, but for the handling of Yoti's callback i.e. data handling.
'''
# from yoti_python_sdk import Client
# from yoti_python_sdk.dynamic_sharing_service.policy import (
#     DynamicPolicyBuilder,
#     SourceConstraintBuilder,
# )
# from yoti_python_sdk.dynamic_sharing_service import DynamicScenarioBuilder
# from yoti_python_sdk.dynamic_sharing_service import create_share_url
# import random

# YOTI_CLIENT_SDK_ID = '754182a1-fbf6-4a20-8615-cf4666f964cc'
# YOTI_PRIVATE_KEY_PATH = data_files['Yoti-For-Kaimai-access-security.pem']
# YOTI_SCENARIO_ID = '26373319-e4fb-47d8-9c68-d23bcb3650a1'
# #Dumb Hardcoded sessionID 
# SESSION_ID ='00000001'
# #/tmp/anvil-data-files/table-866054/Yoti-For-Kaimai-access-security.pem
# yoti_client = Client(YOTI_CLIENT_SDK_ID,YOTI_PRIVATE_KEY_PATH)
