import logging
import pytest

from dotmailer.address_books import AddressBook


log = logging.getLogger(__name__)

@pytest.mark.notdemo
def test_get_by_valid_id(sample_address_book):
    """
    Test to confirm that we can get an address book by a valid ID value.

    :param sample_address_book:
    :return:
    """

    id = sample_address_book.id
    address_book = AddressBook.get_by_id(id)

    assert address_book == sample_address_book
