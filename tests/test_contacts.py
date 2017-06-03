import pytest
from dotmailer.contacts import Contact


def test_create_valid_contact(connection):

    test_data = dict(
        email='test@test.com'
    )

    contact = Contact(**test_data)
    response = contact.create()

    assert isinstance(response, Contact)
    for key, value in test_data.items():
        assert getattr(response, key) == value
