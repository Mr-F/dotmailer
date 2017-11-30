from tests import manually_delete_address_book

from dotmailer.constants import constants
from dotmailer.address_books import AddressBook


def test_get_private(sample_address_book, sample_public_address_book):

    address_books = AddressBook.get_all(address_book_type='Private')
    for book in address_books:
        print book.id, book.name, book.visibility
    assert sample_address_book in address_books
    assert sample_public_address_book not in address_books


def test_get_private_limit(request, connection):

    # Get the current number of public address books in case the account
    # has some data in that we need to take into consideration
    existing_books = AddressBook.get_all(address_book_type='Private')
    offset = len(existing_books)

    # Generate a number of address books
    new_address_books= []
    for x in range(1, 10):
        new_address_books.append(AddressBook(
            name='Address Book %s' % x,
            visibility=constants.VISIBILITY_PRIVATE
        ))
        new_address_books[-1].create()

    # Define a finalizer for the test request so we make sure we clean
    # up after ourselves
    def cleanup():
        for book in new_address_books:
            manually_delete_address_book(connection, book)
    request.addfinalizer(cleanup)

    books = AddressBook.get_private(select=5, skip=offset)

    for book in new_address_books[:5]:
        assert book in books
