import pytest
from dotmailer.contacts import Contact
from dotmailer.constants import constants
from dotmailer.exceptions import ErrorContactNotFound

from .conftest import sample_contact_data

@pytest.mark.parametrize('test_data', [
    sample_contact_data(),
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


@pytest.mark.parametrize('test_data', [
    {} # No email address specified
])
def test_create_invalid_contact(connection, test_data):
    with pytest.raises(KeyError):
        contact = Contact(**test_data)
        contact.create()


@pytest.mark.notdemo
@pytest.mark.parametrize('test_data', [
    {'email': 'new_email@test.com'},
    {'opt_in_type': constants.CONTACT_OPTINTYPE_UNKNOWN},
    {'opt_in_type': constants.CONTACT_OPTINTYPE_VERIFIEDDOUBLE},
    {'opt_in_type': constants.CONTACT_OPTINTYPE_DOUBLE},
    {'opt_in_type': constants.CONTACT_OPTINTYPE_SINGLE},
    {'email_type': constants.CONTACT_EMAILTYPE_HTML},
    {'email_type': constants.CONTACT_EMAILTYPE_PLAIN}
])
def test_update_valid_contact(sample_contact, test_data):

    sample_contact_id = sample_contact.id
    assert sample_contact_id is not None

    sample_contact._update_values(test_data)
    sample_contact.update()

    # Build a list of all keys we should have values for and need to test
    contact = Contact.get_by_id(sample_contact_id)
    for key, value in test_data.items():
        assert getattr(contact, key) == value


@pytest.mark.notdemo
def test_delete_valid_contact(sample_contact):
    sample_contact_id = sample_contact.id
    assert sample_contact_id is not None

    sample_contact.delete()
    assert sample_contact.id is None

    with pytest.raises(ErrorContactNotFound):
        Contact.get_by_id(sample_contact_id)


def test_delete_invalid_contact(connection):
    with pytest.raises(ErrorContactNotFound):
        Contact.delete(999999999)


@pytest.mark.notdemo
def test_delete_contact(connection):
    contact = Contact(
        email='test@test.com'
    )
    contact.create()
    contact.delete()

    contact.create()
    Contact.delete(contact.id)


def test_get_by_email(sample_contact):
    returned_contact = Contact.get_by_email(sample_contact.email)

    attribs = ['id', 'email', 'opt_in_type', 'email_type', 'data_fields']
    for attrib in attribs:
        assert getattr(returned_contact, attrib) == getattr(sample_contact,
                                                            attrib)


def test_get_by_id(sample_contact):
    returned_contact = Contact.get_by_id(sample_contact.id)

    attribs = ['id', 'email', 'opt_in_type', 'email_type', 'data_fields']
    for attrib in attribs:
        assert getattr(returned_contact, attrib) == getattr(sample_contact,
                                                            attrib)

# TODO: Add test for get_address_books
# TODO: Add test for get_all_address_books
# TODO: Add test for get_multiple
# TODO: Add test for get_all
