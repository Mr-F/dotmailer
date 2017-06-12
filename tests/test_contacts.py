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
    """
    Test that creating a contact creates and updates the ID value of
    the contact object correctly.
    
    :param connection: 
    :param test_data: 
    :return: 
    """
    contact = Contact(**test_data)
    assert contact.id is None
    contact.create()
    assert contact.id is not None
    for key, value in test_data.items():
        assert getattr(contact, key) == value

# TODO: Add test for update

@pytest.mark.notdemo
def test_delete_contact(connection):
    contact = Contact(
        email='test@test.com'
    )
    contact.create()
    contact.delete()

    contact.create()
    Contact.delete(contact.id)
