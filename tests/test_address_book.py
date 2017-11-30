import pytest

from dotmailer.address_books import AddressBook
from dotmailer.contacts import Contact


@pytest.mark.notdemo
def test_get_by_id(sample_address_book):
    address_book_id = sample_address_book.id
    assert address_book_id is not None

    returned_book = AddressBook.get_by_id(address_book_id)
    attribs = ['id', 'name', 'visibility']
    for attrib in attribs:
        assert getattr(returned_book, attrib) == getattr(sample_address_book,
                                                         attrib)


# TODO: Add test for get_multiple
# TODO: Add test for get_private
# TODO: Add test for get_public
# TODO: Add test for get_all


@pytest.mark.notdemo
def test_add_contact(sample_address_book):
    # TODO: Look into improving this test
    contact = Contact(email='test_add_contact@test.com')
    sample_address_book.add_contact(contact)
    assert contact.id is not None


def test_add_contact_invalid_address_book(sample_address_book_data,
                                          sample_contact):
    address_book = AddressBook(**sample_address_book_data)
    with pytest.raises(Exception):
        address_book.add_contact(sample_contact)

@pytest.mark.notdemo
def test_delete_contact(sample_address_book):
    contact = Contact(email='test_delete_contact@test.com')
    sample_address_book.add_contact(contact)
    assert contact.id is not None

    sample_address_book.delete_contact(contact)
    # TODO: Figure out how to validate that the user has been removed from the list of contacts associated with this address book


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


# TODO: Add test for delete_multiple_contacts

# TODO: Add test for delete_all_contacts

@pytest.mark.parametrize('name, response', [
    ('', True),
    ('a', True),
    ('a'*128, True),
    ('a'*129, False)
])
def test_valid_name(name, response):
    assert AddressBook.valid_name(name) == response
