import pytest

from dotmailer.contacts import Contact
from dotmailer.exceptions import ErrorContactNotFound

# TODO: Fix this test
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

