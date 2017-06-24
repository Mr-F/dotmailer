import pytest
import ConfigParser
import os

from dotmailer.constants import constants
from dotmailer.account import Account
from dotmailer.address_books import AddressBook
from dotmailer.contacts import Contact


def pytest_addoption(parser):
    parser.addini(
        'username',
        'DotMailer API account username',
        default='demo@apiconnector.com',
    )
    parser.addini(
        'password',
        'DotMailer API account password',
        default='demo'
    )


def pytest_collection_modifyitems(config, items):
    # If the username is that of DotMailer's demo account then update all the
    # tests which will not work as xfails
    if config.getini('username') == 'demo@apiconnector.com':
        for item in items:
            if item.get_marker("notdemo"):
                item.add_marker(pytest.mark.skip(reason='Unable to run against DotMailer\'s demo account'))


@pytest.fixture(scope='session')
def connection(request):
    Account.setup_connection(
        username=request.config.getini('username'),
        password=request.config.getini('password')
    )


@pytest.fixture(scope='session')
def sample_address_book_data():
    return {
        'name': 'Sample address book',
        'visibility': constants.VISIBILITY_PRIVATE
    }


@pytest.fixture(scope='function')
def sample_contact_data():
    return {
        'email': 'sample_user@test.com',
        'opt_in_type': constants.CONTACT_OPTINTYPE_UNKNOWN,
        'email_type': constants.CONTACT_EMAILTYPE_HTML
    }


@pytest.fixture(scope='function')
def sample_address_book(connection, sample_address_book_data):
    sample_address_book = AddressBook(**sample_address_book_data)
    sample_address_book.create()
    return sample_address_book


@pytest.fixture(scope='function')
def sample_contact(sample_contact_data):
    sample_contact = Contact(**sample_contact_data)
    sample_contact.create()
    return sample_contact
