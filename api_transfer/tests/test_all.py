"""Unit test functions for the api_transfer app"""
import pytest
from api_transfer.utilities.github_handler import GitHubHandler
from api_transfer.utilities.freshdesk_handler import FreshDeskHandler
from api_transfer.utilities.adaptor import DataAdaptor


@pytest.fixture
def ghconnector():
    '''Returns a GitHubHandler object'''
    return GitHubHandler('user')

@pytest.fixture
def fdconnector():
    '''Returns a FreshdeskHandler object'''
    return FreshDeskHandler()

@pytest.fixture
def adaptor():
    '''Returns a DataAdaptor object'''
    return DataAdaptor({
        "name"              : "name",
        "email"             : "email",
        "location"          : "address",
        "twitter_username"  : "twitter_id"
    })

def test_gh_create_users_url_all(ghconnector):
    assert ghconnector.create_users_url() == ghconnector.base_url + '/users'

def test_gh_create_users_url_single(ghconnector):
    assert ghconnector.create_users_url('test') == ghconnector.base_url + '/users/test'


def test_fd_add_subdomain_to_url(fdconnector):
    fdconnector.set_subdomain('test')
    assert fdconnector.base_url == 'https://test.freshdesk.com/api/v2'

def test_adaptor_github_to_freshdesk_remaping(adaptor):
    github_data = {
        'name'              : 'John',
        'email'             : 'john@test',
        'location'          : 'L.A.',
        'twitter_username'  : 'tweety',
        # This will be skipped:
        'random_field'      : 'just any value'
    }
    result = adaptor.covert_github_to_freshdesk(github_data)
    expected_freshdesk_data = {
        'name'          : 'John',
        'email'         : 'john@test',
        'address'       : 'L.A.',
        'twitter_id'    : 'tweety',
        # this will be added
        'description'   : 'Transfer from GitHub'
    }
    assert result == expected_freshdesk_data
