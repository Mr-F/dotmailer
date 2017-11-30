import logging
import pytest

from dotmailer.address_books import AddressBook
from dotmailer.exceptions import ErrorAddressbookNotFound, ErrorAddressbookNotwritable


log = logging.getLogger(__name__)

@pytest.mark.notdemo
def test_delete_valid_address_book(sample_address_book):
    """
    Test to confirm that the delete functionality for address books 
    behaves  correctly.  Calling the delete on an address book should 
    update the ID attribute of the address book to be null, whilst also
    triggering DotMailer to remove the address book from the account.
    
    :param sample_address_book: 
    :return: 
    """
    address_book_id = sample_address_book.id
    assert address_book_id is not None, 'Sample address book doesn\'t' \
                                        ' have an ID value.'

    # Tell DotMailer that you wish to delete the address book
    sample_address_book.delete()
    assert sample_address_book.id is None, 'Address book ID was not ' \
                                           'nulled'

    # Finally, confirm that address book doesn't exists any more
    with pytest.raises(ErrorAddressbookNotFound):
        AddressBook.get_by_id(address_book_id)


def test_delete_invalid_address_book():
    with pytest.raises(ErrorAddressbookNotFound):
        AddressBook.delete(999999999)


@pytest.mark.notdemo
@pytest.mark.parametrize('book_name', ['Test'])
def test_delete_protected_address_book(book_name):
    """
    Test to confirm that if the delete end point is called on one of the
    protected address books (All Contacts and Test), then the
    appropriate exception is raised.

    :param book_name:
    :return:
    """

    test_book = None

    # Get a list of all address books in the account.
    books = AddressBook.get_all()
    print books
    # Find the test address book and grab it's ID value
    for book in books:
        log.info("Address book: {}".format(book.name))
        print book.name
        if book.name == book_name:
            test_book = book
            break

    # Assert that the test book has been found, otherwise stop here
    assert test_book is not None

    # Confirm that the class method version raises the correct exception
    with pytest.raises(ErrorAddressbookNotwritable):
        AddressBook.delete(test_book.id)

    # Confirm that the instance method version raises the correct
    # exception
    with pytest.raises(ErrorAddressbookNotwritable):
        test_book.delete()
