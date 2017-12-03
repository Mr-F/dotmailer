import pytest

from dotmailer.address_books import AddressBook
from dotmailer.contacts import Contact


@pytest.mark.notdemo
def test_delete_contact(sample_address_book):
    # contact = Contact(email='test_delete_contact@test.com')
    # sample_address_book.add_contact(contact)
    # assert contact.id is not None
    #
    # sample_address_book.delete_contact(contact)
    # # TODO: Figure out how to validate that the user has been removed from the list of contacts associated with this address book
    assert False


def test_delete_contact_invalid_address_book(sample_address_book_data,
                                             sample_contact):
    address_book = AddressBook(**sample_address_book_data)
    with pytest.raises(Exception):
        address_book.delete_contact(sample_contact)

@pytest.mark.notdemo
def test_delete_contact_invalid_contact(sample_address_book,
                                        sample_contact_data):
    contact = Contact(**sample_contact_data)
    with pytest.raises(Exception):
        sample_address_book.delete_contact(contact)
