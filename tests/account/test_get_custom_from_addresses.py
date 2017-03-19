from dotmailer.account import Account


def test_custom_from_field(connection):
    """

    :param connection: This is a fixture call which will create attempt
    to create an active connection to their API server, for the test
    to run.

    :return:
    """
    response = Account.get_custom_from_addresses()
    assert isinstance(response, list)
    if len(response) > 0:
        assert 'id' in response[0]
        assert 'email' in response[0]

    # TODO: Possibly need to look to expand this test case so that if no value is return then we create one to test against

