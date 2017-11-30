import pytest

from dotmailer.address_books import AddressBook
from dotmailer.constants import constants
from tests import manually_delete_address_book
from tests.conftest import sample_address_book_data


@pytest.mark.parametrize('test_data', [
    sample_address_book_data(),
    {'name': 'Test address book'},
    {'name': 'Test address book', 'visibility': constants.VISIBILITY_PRIVATE}
])
def test_create_valid_address_book(connection, test_data):
    """
    Test to confirm that when submitting various different valid address
    books that they are created.
    
    :param connection: 
    :param test_data:
    :return: 
    """

    address_book = AddressBook(**test_data)
    address_book.create()
    assert address_book.id is not None

    # Attempt to delete the address book created by the test
    manually_delete_address_book(connection, address_book)


@pytest.mark.parametrize('test_data', [
    {'visibility': constants.VISIBILITY_PRIVATE},
    {'name': 'a' * 200},
    {}
])
def test_create_invalid_address_book(test_data):
    """
    Test to confirm that when attempting to create an invalid address
    book, that an exception is raised.
     
    :param test_data: 
    :return: 
    """

    with pytest.raises((Exception, KeyError)):
        address_book = AddressBook(**test_data)
        address_book.create()
