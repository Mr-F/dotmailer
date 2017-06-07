import pytest
from dotmailer.contacts import Contact
from dotmailer.constants import constants


@pytest.mark.parametrize('test_data', [
    {'email': 'test@test.com'},
    {'email': 'test@test.com', 'opt_in_type': constants.CONTACT_OPTINTYPE_UNKNOWN},
    {'email': 'test@test.com', 'opt_in_type': constants.CONTACT_OPTINTYPE_SINGLE},
    {'email': 'test@test.com', 'opt_in_type': constants.CONTACT_OPTINTYPE_DOUBLE},
    {'email': 'test@test.com', 'opt_in_type': constants.CONTACT_OPTINTYPE_VERIFIEDDOUBLE},
    {'email': 'test@test.com', 'email_type': constants.CONTACT_EMAILTYPE_HTML},
    {'email': 'test@test.com', 'email_type': constants.CONTACT_EMAILTYPE_PLAIN},
    {'email': 'test@test.com',  'opt_in_type': constants.CONTACT_OPTINTYPE_DOUBLE, 'email_type': constants.CONTACT_EMAILTYPE_PLAIN},
])
def test_create_valid_contact(connection, test_data):

    contact = Contact(**test_data)
    response = contact.create()

    assert isinstance(response, Contact)
    for key, value in test_data.items():
        assert getattr(response, key) == value
