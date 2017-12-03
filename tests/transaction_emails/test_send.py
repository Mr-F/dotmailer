import pytest

from dotmailer.transactional_emails import TransactionEmail


def test_valid_send(connection):

    test_data = dict(
        to_addresses='mr-f@mr-f.org',
        subject='Hello, world!',
        from_address='demo@apiconnector.com',
        html_content='<div>Hello, world!<a href="http://$UNSUB$"> Unsubscribe '
                     'from this newsletter</a></div>',
        plain_text_content='Hello, world! $UNSUB$'
    )

    transactional_email = TransactionEmail(**test_data)
    transactional_email.send()
    # The only thing to test is that no exception is raised


def test_invalid_send(connection):
    test_data = {
        'to_addresses': 'no_email',
        'subject': 'Hello, world!',
        'from_address': 'demo@apiconnector.com',
        'html_content': '<a href="http://$UNSUB$">Unsubscribe</a>',
        'plain_text_content': '$UNSUB$'
    }
    transactional_email = TransactionEmail(**test_data)
    # TODO: Confirm what should happen if bad data is sent to DotMailer.  Shouldn't it return an error?
    with pytest.raises(Exception):
        transactional_email.send()
