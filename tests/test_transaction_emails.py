import pytest
import datetime
from dotmailer.transactional_emails import TransactionEmail


def test_valid_send(connection):

    test_data = dict(
        to_address='mr-f@mr-f.org',
        subject='Hello, world!',
        from_address='demo@apiconnector.com',
        html_content='<div>Hello, world!<a href="http://$UNSUB$"> Unsubscribe '
                     'from this newsletter</a></div>',
        plain_text_content='Hello, world! $UNSUB$'
    )

    transactional_email = TransactionEmail(**test_data)
    transactional_email.send()
    # The only thing to test is that no exception is raised


@pytest.mark.parametrize('aggregate_by', ['AllTime', 'Month', 'Week', 'Day'])
def test_get_stats(connection, aggregate_by):
    """
    Test to confirm that all the expected keys are returned from the API when
    data is requested.  This test does not validate the actual values returned
    just that the keys we expected to be there are.
    
    :param connection: 
    :param aggregate_by:
    :return: 
    """
    expected_keys = [
        'start_date', 'end_date', 'num_sent', 'num_delivered', 'num_opens',
        'num_clicks', 'num_isp_complaints', 'num_bounces'
    ]

    response = TransactionEmail.get_stats(
        datetime.date(2016, 1, 1),
        datetime.date(2016, 12, 31),
        aggregate_by
    )

    # Loop through the list of aggregated data points, checking that each
    # entry has all the expected keys
    for group in response:
        for key in expected_keys:
            assert key in group
