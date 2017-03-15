import pytest
import ConfigParser
import os

from dotmailer.account import Account

@pytest.fixture(scope='session')
def connection(request):
    config = ConfigParser.ConfigParser()
    config.read(os.path.abspath(request.config.inicfg.config.path))
    Account.create_connection(
        username=config.get('pytest', 'username'),
        password=config.get('pytest', 'password')
    )
