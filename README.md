# The task

Create a command line Python program, which retrieves the information of a GitHub User and creates a new Contact or updates an existing contact in Freshdesk, using their respective APIs.

- Use GitHub Rest API v3. Documentation is available at https://developer.github.com/v3/
- Use Freshdesk API v2. Documentation is available at https://developers.freshdesk.com/api/
- Your program should be able to get GitHub user login (username) and Freshdesk subdomain from the command line.
- For authentication assume GitHub personal access token is given in GITHUB_TOKEN environmental variable and Freshdesk API key is given in FRESHDESK_TOKEN environmental variable.
- Transfer all compatible fields from the GitHub User to the Freshdesk Contact by your judgment
- Please provide unit tests for the main program functionality. Create a separate module for the unit tests.
- You may use either Python 2.7 or Python 3.x.
- You may also use any Python libraries which will help you with the task, such as requests or mock, except for API clients for Freshdesk or GitHub.
- While you may create trial accounts in GitHub and Freshdesk, this is not a requirement. You can use the examples from the documentation as test data.
- Please provide a README.md file with instructions on how to run the Python program and the tests.

# App Description

The api_transfer package is a command line python3 utility that gets an user from the publicly available users in GitHub, extracts their available data and using it creates or updates a contact in the FreshDesk web platform.

Running the utility requires existence of accounts in github and in Freshdesk.  
GitHub allows creation of free accounts. The GitHub account is used to access the publicly available users and list their publicly available profile data. From that list specific account login name could be selected and passed to the api_transfer tool to create/modified its FreshDesk account. The access to the github API requires username and access token.

When user profile data is retrieved from GitHub it is transformed to the required data input form required by the Fresahdesk API using an adaptor class. The mapping of the fields is a part ot the app's configuration data.
After the data is prepared the FreshDesk connector checks if account with the given email address exists. If the account exists the account profile data is updated else a new account is created.
FreshDesk allows creation of a test account for a month trial period. Each account creates a subdomain in the freshdesk web platform. 
The access to the freshdesk requires API key.

The package configuration file is the config.json file that contains the user that is contacting the github API and the fields that will be extracted/migrated between the two platforms. This is an example of such file:


{
    "mappings" : {
        "name"              : "name",
        "email"             : "email",
        "location"          : "address",
        "twitter_username"  : "twitter_id"
    },
    "ghuser" : "githubuser"
}


The tool requires two command line arguments:
--gh_user - the github login of the user that will be migrated
--fd_subdomain - the freshdesk subdomain name (could be moved into the config.json too)

# How to run

## Prerequisites  

In order to run the tool, following setup must be made:
1. In the configuration file resources/config.json the github username must be provided.
2. In the same file mapping fields must be provided.
3. The github user's access token must be set as environmental variable GITHUB_TOKEN
4. The Freshdesk api key must be set as environmental variable FRESHDESK_TOKEN

## Setting variables

Following credentials could be used to test the app:  

export GITHUB_TOKEN=   
export FRESHDESK_TOKEN=  

## Running

python3 -m api_transfer --gh_user [githubuserlogin] --fd_subdomain [subdomain]

# How to test
use pytest from command line

pytest
