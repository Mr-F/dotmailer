import pytest

from dotmailer.address_books import AddressBook
from dotmailer.contacts import Contact


@pytest.mark.notdemo
def test_add_contact(sample_address_book):

    contact = Contact(email='test_add_contact@test.com')
    sample_address_book.add_contact(contact)
    assert contact.id is not None

    # Clean up by removing the contact afterwards
    contact.delete()


def test_add_contact_invalid_address_book(sample_address_book_data,
                                          sample_contact):
    address_book = AddressBook(**sample_address_book_data)
    with pytest.raises(Exception):
        address_book.add_contact(sample_contact)
