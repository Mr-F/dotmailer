import pytest

from dotmailer.address_books import AddressBook
from dotmailer.constants import constants


def _confirm_address_book_valid(address_book):
    address_book_id = address_book.id
    assert address_book_id is not None
    return address_book_id

@pytest.mark.notdemo
@pytest.mark.parametrize('test_data', [
    {'name': 'New Value', 'visibility': constants.VISIBILITY_PUBLIC},
    {'name': 'New Value2', 'visibility': constants.VISIBILITY_PRIVATE}
])
def test_update_valid_address_book(sample_address_book, test_data):
    """
    Test function to confirm that submitting new values to an existing 
    address book, will result in the values on the server being updated.
    
    This test will not work if you are using the demo account creditials.
    :param sample_address_book: 
    :param test_data: 
    :return: 
    """
    address_book_id = _confirm_address_book_valid(sample_address_book)

    # Force an update of the address book
    sample_address_book._update_values(test_data)
    sample_address_book.update()

    # Finally query the server for the address book and confirm the new
    # values where stored.
    address_book = AddressBook.get_by_id(address_book_id)
    for key, value in test_data.items():
        assert getattr(address_book, key) == value



@pytest.mark.notdemo
def test_update_invalid_address_book_name(sample_address_book):

    _confirm_address_book_valid(sample_address_book)
    sample_address_book._update_values({'name': 'a' * 200})
    with pytest.raises(Exception):
        sample_address_book.update()
