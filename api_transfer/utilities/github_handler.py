import requests
from requests.auth import HTTPBasicAuth
import os

class GitHubHandler:
    def __init__(self, username):
        self.base_url = 'https://api.github.com'
        self.username = username

    def get_users(self, user_id=None):
        """Method getting:
        - the list of available users, if user_id flg is None;
        - given user's information if the user_id is provided
        """
        url=self.create_users_url(user_id)
        response = requests.get(url, auth=self.get_auth())
        response.raise_for_status()
        if not response.json()['email']:
            raise Exception('No email for that github account')
        return response.json()

    def create_users_url(self, user_id=None):
        return '{baseurl}/users{usrname}'.format(
                baseurl=self.base_url,
                usrname='' if not user_id else '/'+user_id
            )

    def get_auth(self):
        api_key=None 
        if os.getenv('GITHUB_TOKEN'):
            api_key = os.getenv('GITHUB_TOKEN')
        else:
            raise Exception('No GITHUB_TOKEN defined')
        return HTTPBasicAuth(self.username,api_key)
