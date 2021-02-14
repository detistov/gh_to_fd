import os
import argparse
import json
from pathlib import Path
import traceback
from requests.exceptions import HTTPError
from api_transfer.utilities.github_handler import GitHubHandler
from api_transfer.utilities.freshdesk_handler import FreshDeskHandler
from api_transfer.utilities.adaptor import DataAdaptor

def run():
    parser = argparse.ArgumentParser(prog='api_transfer', description='A tool to get user data from GitHub and create FreshDesk contact')
    parser.add_argument('--gh_user', help='The GitHub username to migrate', required=True)
    parser.add_argument('--fd_subdomain', help='The FreshDesk subdomain', required=True)
    args = parser.parse_args()
    print('Input parameters')
    print(json.dumps(vars(args), indent=4))
    configuration = None
    try:
        config_path = Path(__file__).parent
        config_path = os.path.join(config_path,'resources/config.json')
        with open(config_path, 'r') as f:
            configuration = json.loads(f.read())
        print("*** CONFIGURATION ***")
        print(json.dumps(configuration,indent=4))
        
        # Instantiating the GitHubConnector
        github = GitHubHandler(configuration['ghuser'])

        githubres = github.get_users(args.gh_user)
        print("** user data **")
        print(json.dumps(githubres, indent=4))

        # Instantiating the adaptor
        adaptor = DataAdaptor(configuration['mappings'])
        new_data = adaptor.covert_github_to_freshdesk(githubres)
        print("** converted data to FD **")
        print(json.dumps(new_data, indent=4))

        # Instantiating the FreshDesk connector
        freshdesk = FreshDeskHandler()
        freshdesk.set_subdomain(args.fd_subdomain)
        res = None
        if 'email' in new_data.keys():
            res = freshdesk.get_contact_id(new_data['email'])
        if res:
            print('Updating the contact ...', end='')
            fdresponse = freshdesk.update_contact(res,new_data)
            print('done')
        else:
            print('No contact with this email found. Creating a new contact ...')
            fdresponse = freshdesk.create_contact(new_data)
            print('done')

        print(json.dumps(fdresponse,indent=4))
        print("\nDONE\n")
    except HTTPError as httperror:
        print('Error: ', httperror)
    except Exception as e:
        print('ERROR: ', e)
        print('\nCould not complete migration due to errors!')
        #traceback.print_exc()


        
