"""FreshDesk connection manager class
"""
import os
import urllib
import requests
from requests.auth import HTTPBasicAuth
import json

class FreshDeskHandler:
    def __init__(self):
        self.base_url_model='https://{dom}.freshdesk.com/api/v2'
        self.headers = {'Content-Type':'application/json'}
        self.dase_url = None

    def set_subdomain(self,subdomain)->None:
        """Setting the subdomain"""
        self.base_url = self.base_url_model.format(dom=subdomain)

    def check_base_url(self):
        """Checking if the base url is created"""
        if not self.base_url:
            raise Exception('No base URL created')

    def get_contact_id(self, email):
        """Looking for contact by email"""
        self.check_base_url()
        response = requests.get(
                                self.base_url + '/contacts',
                                auth=self.get_auth(), 
                                headers=self.headers, 
                                params={"email" : email}
                                )
        response.raise_for_status()
        print('Contacts containing the email: ', email)
        print(json.dumps(response.json(),indent=4))
        if len(response.json()) > 1:
            print('Multiple contacts with this email')
            raise Exception('Multiple contacts to update')
        return None if not response.json() else response.json()[0]['id']

    def create_contact(self, payload):
        """Create a new contact"""
        self.check_base_url()
        response=requests.post( self.base_url + '/contacts', 
                                auth=self.get_auth(), 
                                headers=self.headers, 
                                data=json.dumps(payload)
                              )
        response.raise_for_status()
        return response.json()

    def update_contact(self, contact_id, data):
        """Update contact info"""
        self.check_base_url()
        response=requests.put( self.base_url + '/contacts/{}'.format(contact_id), 
                                auth=self.get_auth(), 
                                headers=self.headers, 
                                data=json.dumps(data)
                              )
        response.raise_for_status()
        return response.json()

    def get_auth(self):
        """Preparing the authentication data"""
        apikey = os.getenv('FRESHDESK_TOKEN')
        if apikey:
            return HTTPBasicAuth(apikey,'')
        raise Exception('No FRESHDESK_TOKEN defined')


    