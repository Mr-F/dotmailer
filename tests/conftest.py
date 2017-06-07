import pytest
import ConfigParser
import os

from dotmailer.account import Account


def pytest_addoption(parser):
    parser.addini(
        'username',
        'DotMailer API account username',
        default='demo@apiconnector.com',
    )
    parser.addini(
        'password',
        'DotMailer API account password',
        default='demo'
    )


def pytest_collection_modifyitems(config, items):
    # If the username is that of DotMailer's demo account then update all the
    # tests which will not work as xfails
    if config.getini('username') == 'demo@apiconnector.com':
        for item in items:
            if item.get_marker("notdemo"):
                item.add_marker(pytest.mark.skip(reason='Unable to run against DotMailer\'s demo account'))


@pytest.fixture(scope='session')
def connection(request):
    config = ConfigParser.ConfigParser()
    config.read(os.path.abspath(request.config.inicfg.config.path))
    Account.setup_connection(
        username=config.get('pytest', 'username'),
        password=config.get('pytest', 'password')
    )
