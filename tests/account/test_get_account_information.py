from dotmailer.account import Account


def test_get_account_information(connection):
    """
    Test function to confirm that once a connection is setup, that
    calling the get account information function returns a JSON
    dictionary which contains at least the `id` and `properties` keys.

    :param connection: This is a fixture call which will create attempt
    to create an active connection to their API server, for the test
    to run.

    :return:
    """
    response = Account.get_account_information()

    assert 'id' in response
    assert 'properties' in response

    expected_properties = [
        # 'AvailableEmailSendsCredits',
        # 'AvailableSmsSendsCredits',
        'APILocale',
        'ListManagedUsers',
        'Name',
        'MainMobilePhoneNumber',
        'MainEmail',
        'ApiCallsInLastHour',
        'ApiCallsRemaining',
        'ApiEndpoint'

    ]
    response_properties = [entry['name'] for entry in response['properties']]
    for key in expected_properties:
        assert key in response_properties
