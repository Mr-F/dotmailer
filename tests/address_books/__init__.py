import pytest

from dotmailer.address_books import AddressBook

@pytest.mark.parametrize('name, response', [
    ('', True),
    ('a', True),
    ('a'*128, True),
    ('a'*129, False)
])
def test_valid_name(name, response):
    assert AddressBook.valid_name(name) == response
