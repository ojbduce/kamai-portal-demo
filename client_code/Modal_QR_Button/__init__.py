from ._anvil_designer import Modal_QR_ButtonTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js


class Modal_QR_Button(Modal_QR_ButtonTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Add click event handler to the button DOM node
        self.qr_code_button = anvil.js.get_dom_node(self)
        self.qr_code_button.addEventListener('click', self.on_qr_button_click)

    def on_qr_button_click(self, event):
        # Call server function to create the Yoti session and get share_url
        share_data = anvil.server.call('create_yoti_share_session')
        client_sdk_id = share_data['clientSdkId']
        share_url = share_data['shareUrl']

        # Pass values to the JavaScript function to initialize Yoti WebShare
        self.call_js('initializeYotiWebShare', client_sdk_id, share_url)

    def form_show(self, **event_args):
        """This method is called when the form is shown on the page"""
        pass
