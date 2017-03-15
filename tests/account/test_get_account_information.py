import pytest
from dotmailer.account import Account

def test_get_account_information(connection):
    """
    Test function to confirm that once a connection is setup, that
    calling the get account information function returns a JSON
    dictionary which contains at least the `id` and `properties` keys.

    :param connection:
    :return:
    """
    response = Account.get_account_information()

    assert 'id' in response
    assert 'properties' in response
