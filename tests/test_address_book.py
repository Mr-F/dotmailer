import pytest
from dotmailer.constants import constants
from dotmailer.address_books import AddressBook

@pytest.mark.parametrize('test_data', [
    {'name': 'Test address book'},
    {'name': 'Test address book', 'visibility': constants.VISIBILITY_PRIVATE},
    {'name': 'Test address book', 'visibility': constants.VISIBILITY_PUBLIC}
])
def test_create_valid_address_book(connection, test_data):
    """
    Test to confirm that when submitting various different valid address books
    that they are created.
    
    :param connection: 
    :return: 
    """
    address_book = AddressBook(**test_data)

    assert isinstance(address_book, AddressBook)
    for key, value in test_data.items():
        assert getattr(address_book, key) == value


@pytest.mark.parametrize('test_data', [
    {'visibility': constants.VISIBILITY_PRIVATE},
    {'name': 'a' * 200}
])
def test_create_invalid_address_book(connection, test_data):

    with pytest.raises((Exception, KeyError)):
        address_book = AddressBook(**test_data)
        address_book.create()
