import pytest
import ConfigParser
import os

from dotmailer.account import Account
from dotmailer.address_books import AddressBook
from dotmailer.campaigns import Campaign
from dotmailer.constants import constants
from dotmailer.contact_data_fields import ContactDataField
from dotmailer.contacts import Contact
from dotmailer.templates import Template

from tests.campaigns import sample_campaign_data
from tests.contact_data_fields import sample_contact_data_field_data
from tests.templates import sample_template_data
from tests import manually_delete_address_book, manually_delete_contact, \
    manually_delete_campaign, manually_delete_contact_data_field

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
    parser.addini(
        'from_address',
        'The from_address specified in your DotMailer account'
    )


def pytest_collection_modifyitems(config, items):
    # If the username is that of DotMailer's demo account then update all the
    # tests which will not work as xfails
    if config.getini('username') == 'demo@apiconnector.com':
        for item in items:
            if item.get_marker("notdemo"):
                item.add_marker(pytest.mark.skip(reason='Unable to run against DotMailer\'s demo account'))


@pytest.fixture(scope='session')
def account_from_address(request):
    return request.config.getini('from_address')


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

    def _finalizer():
        manually_delete_contact(connection, contact)
    request.addfinalizer(_finalizer)

    return contact


@pytest.fixture(scope='function')
def sample_template(request, connection):
    template = Template(**sample_template_data())
    template.create()

    # Currently DotMailer's API doesn't support deletion of templates so
    # no rollback finalizer to add here.

    return template


@pytest.fixture(scope='function')
def sample_campaign(request, connection, account_from_address):
    data = sample_campaign_data()
    data['from_address']['email'] = account_from_address
    campaign = Campaign(**data)
    campaign.create()

    def _finalizer():
        manually_delete_campaign(connection, campaign)
    request.addfinalizer(_finalizer)

    return campaign


@pytest.fixture(scope='function')
def sample_contact_data_field(request, connection):
    contact_data_field = ContactDataField(**sample_contact_data_field_data())
    contact_data_field.create()
    def _finalizer():
        manually_delete_contact_data_field(connection, contact_data_field)
    request.addfinalizer(_finalizer)

    return contact_data_field
