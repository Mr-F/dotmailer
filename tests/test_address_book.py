import pytest
from dotmailer.constants import constants
from dotmailer.address_books import AddressBook
from dotmailer.exceptions import (ErrorAddressbookNotFound,
                                  ErrorAddressbookNotwritable)


_sample_address_book_data = {
    'name': 'Sample address book',
    'visibility': constants.VISIBILITY_PRIVATE
}


@pytest.mark.parametrize('test_data', [
    {'name': 'Test address book'},
    {'name': 'Test address book', 'visibility': constants.VISIBILITY_PRIVATE},
    {'name': 'Test address book', 'visibility': constants.VISIBILITY_PUBLIC}
])
def test_create_valid_address_book(connection, test_data):
    """
    Test to confirm that when submitting various different valid address
    books that they are created.
    
    :param connection: 
    :return: 
    """
    address_book = AddressBook(**test_data)
    address_book.create()
    assert address_book.id is not None

@pytest.mark.parametrize('test_data', [
    {'visibility': constants.VISIBILITY_PRIVATE},
    {'name': 'a' * 200}
])
def test_create_invalid_address_book(connection, test_data):

    with pytest.raises((Exception, KeyError)):
        address_book = AddressBook(**test_data)
        address_book.create()


@pytest.mark.notdemo
@pytest.mark.parametrize('test_data',[
    {'name': 'New Value', 'visibility': constants.VISIBILITY_PUBLIC}
])
def test_update_valid_address_book(connection, test_data):
    """
    Test function to confirm that submitting new values to an existing 
    address book, will result in the values on the server being updated.
    
    This test will not work if you are using the demo account creditials.
    :param connection: 
    :param test_data: 
    :return: 
    """
    sample_address_book = AddressBook(**_sample_address_book_data)
    sample_address_book.create()
    address_book_id = sample_address_book.id
    assert address_book_id is not None

    # Force an update of the address book
    for key, value in test_data.items():
        setattr(sample_address_book, key, value)
    sample_address_book.update()

    # Finally query the server for the address book and confirm the new values
    # where stored.
    address_book = AddressBook.get(address_book_id)
    for key, value in test_data.items:
        assert getattr(address_book_id, key) == value


@pytest.mark.notdemo
def test_delete_valid_address_book(connection):
    """
    Test to confirm that the delete functionality for address books 
    behaves  correctly.  Calling the delete on an address book should 
    update the ID attribute of the address book to be null, whilst also
    triggering DotMailer to remove the address book from the account.
    
    :param connection: 
    :return: 
    """
    address_book = AddressBook(**_sample_address_book_data)
    address_book.create()
    address_book_id = address_book.id
    assert address_book_id is not None, 'Sample address book doesn\'t have an' \
                                        ' ID value.'

    # Tell DotMailer that you wish to delete the address book
    address_book = AddressBook.get(address_book_id)
    address_book = address_book.delete()
    assert address_book.id is None, "Address book ID was not nulled"

    # Finally
    with pytest.raises(ErrorAddressbookNotFound):
        AddressBook.get(address_book_id)


def test_delete_invalid_address_book(connection):
    with pytest.raises(ErrorAddressbookNotFound):
        AddressBook.delete(999999999)


@pytest.mark.notdemo
@pytest.mark.parametrize('book_name', ['All Contacts', 'Test'])
def test_delete_protected_address_book(connection, book_name):
    """
    Test to confirm that if the delete end point is called on one of the
    protected address books (All Contacts and Test), then the 
    appropriate exception is raised.
    
    :param connection: 
    :param book_name: 
    :return: 
    """

    test_book = None

    # Get a list of all address books in the account.
    books = AddressBook.get_all()

    # Find the test address book and grab it's ID value
    for book in books:
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
