import pytest

from tests import manually_delete_contact

from dotmailer.contacts import Contact
from dotmailer.constants import constants


@pytest.mark.parametrize('test_data', [
    # sample_contact_data(),
    {'email': 'test1@test.com'},
    {'email': 'test2@test.com',
     'opt_in_type': constants.CONTACT_OPTINTYPE_UNKNOWN},
    {'email': 'test3@test.com',
     'opt_in_type': constants.CONTACT_OPTINTYPE_SINGLE},
    {'email': 'test4@test.com',
     'opt_in_type': constants.CONTACT_OPTINTYPE_DOUBLE},
    # {'email': 'test5@test.com',
    #  'opt_in_type': constants.CONTACT_OPTINTYPE_VERIFIEDDOUBLE},
    {'email': 'test6@test.com', 'email_type': constants.CONTACT_EMAILTYPE_HTML},
    {'email': 'test7@test.com',
     'email_type': constants.CONTACT_EMAILTYPE_PLAIN},
    {'email': 'test8@test.com',
     'opt_in_type': constants.CONTACT_OPTINTYPE_DOUBLE,
     'email_type': constants.CONTACT_EMAILTYPE_PLAIN},
])
def test_create_valid_contact(request, connection, test_data):
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
    # This way even if the test fails the test should clean up anything it
    # created for us
    # def cleanup():
    #     manually_delete_contact(connection, contact)
    # request.addfinalizer(cleanup)

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
