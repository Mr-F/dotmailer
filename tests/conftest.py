import pytest
import ConfigParser
import os

from dotmailer.constants import constants
from dotmailer.account import Account
from dotmailer.address_books import AddressBook
from dotmailer.contacts import Contact

from tests import manually_delete_address_book, manually_delete_contact

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


@pytest.fixture(scope='session', autouse=True)
def connection(request):
    return Account.setup_connection(
        username=request.config.getini('username'),
        password=request.config.getini('password')
    )



@pytest.fixture(scope='session')
def sample_address_book_data():
    return {
        'name': 'Sample address book',
        'visibility': constants.VISIBILITY_PRIVATE
    }

@pytest.fixture(scope='session')
def sample_public_address_book_data():
    return {
        'name': 'Sample private address book',
        'visibility': constants.VISIBILITY_PUBLIC
    }


@pytest.fixture(scope='function')
def sample_contact_data():
    return {
        'email': 'test0@test.com',
        'opt_in_type': constants.CONTACT_OPTINTYPE_UNKNOWN,
        'email_type': constants.CONTACT_EMAILTYPE_HTML
    }


@pytest.fixture(scope='function')
def sample_address_book(request, connection, sample_address_book_data):
    address_book = AddressBook(**sample_address_book_data)
    address_book.create()

    # Adding a finalizer so that we can remove the address book so that
    # it would foul up other test cases or test runs.
    def _finalizer():
        manually_delete_address_book(connection, address_book)
    request.addfinalizer(_finalizer)

    return address_book


@pytest.fixture(scope='function')
def sample_public_address_book(request, connection,
                                sample_public_address_book_data):
    address_book = AddressBook(**sample_public_address_book_data)
    address_book.create()

    # Adding a finalizer so that we can remove the address book so that
    # it would foul up other test cases or test runs.
    def _finalizer():
        manually_delete_address_book(connection, address_book)
    request.addfinalizer(_finalizer)

    return address_book


@pytest.fixture(scope='function')
def sample_contact(request, connection, sample_contact_data):
    contact = Contact(**sample_contact_data)
    contact.create()

    print "Contact created", contact.id
    def _finalizer():
        print "Trying to delete contact"
        manually_delete_contact(connection, contact)
    request.addfinalizer(_finalizer)

    return contact
