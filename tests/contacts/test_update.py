import pytest

from dotmailer.contacts import Contact
from dotmailer.constants import constants


@pytest.mark.notdemo
@pytest.mark.parametrize('test_data', [
    {'email': 'testing1@test.com'},
    # {'opt_in_type': constants.CONTACT_OPTINTYPE_UNKNOWN},
    # # {'opt_in_type': constants.CONTACT_OPTINTYPE_VERIFIEDDOUBLE},
    # {'opt_in_type': constants.CONTACT_OPTINTYPE_DOUBLE},
    # {'opt_in_type': constants.CONTACT_OPTINTYPE_SINGLE},
    # {'email_type': constants.CONTACT_EMAILTYPE_HTML},
    # {'email_type': constants.CONTACT_EMAILTYPE_PLAIN}
])
def test_update_valid_contact(sample_contact, test_data):

    sample_contact_id = sample_contact.id
    assert sample_contact_id is not None

    # sample_contact._update_values(test_data)
    sample_contact.email = 'new_value@test.com'
    sample_contact.update()

    # Build a list of all keys we should have values for and need to test
    # contact = Contact.get_by_id(sample_contact_id)
    # for key, value in test_data.items():
    #     assert getattr(contact, key) == value
