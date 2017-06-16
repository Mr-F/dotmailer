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


@pytest.mark.parametrize('test_data', [
    {} # No email address specified
])
def test_create_invalid_contact(connection, test_data):
    with pytest.raises(KeyError):
        contact = Contact(**test_data)
        contact.create()


@pytest.mark.notdemo
@pytest.mark.parametrize('original_data, update_data', [
    (None, {})
])
def test_update_valid_contact(connection, original_data, update_data):
    # TODO: Finish this test off working out test data to push through it
    if original_data is None:
        original_data = {
            'email': 'test@test.com',
            'opt_in_type': constants.CONTACT_OPTINTYPE_UNKNOWN,
            'email_type': constants.CONTACT_EMAILTYPE_PLAIN
        }
    contact = Contact(**original_data)
    contact.create()
    contact._update_values(update_data)
    contact.update()

    # Build a list of all keys we should have values for and need to test
    keys = set(original_data.keys())
    keys.update(update_data.keys())
    ignore_list = ['data_fields']
    for key in keys:
        if key in ignore_list:
            continue
        value = getattr(contact, key)
        if key in update_data:
            assert type(update_data[key]) == type(value)
            assert update_data[key] == value
        else:
            assert type(original_data[key]) == type(value)
            assert original_data[key] == value


@pytest.mark.notdemo
def test_delete_contact(connection):
    contact = Contact(
        email='test@test.com'
    )
    contact.create()
    contact.delete()

    contact.create()
    Contact.delete(contact.id)
