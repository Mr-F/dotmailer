import pytest

from dotmailer.contact_data_fields import ContactDataField


@pytest.mark.parametrize('value, response', [
    ('a', True),
    ('aa', True),
    ('a' * 10, True),
    ('a' * 20, True),
    ('customName', True),
    ('custom-name', True),
    ('custom_name', True),
    ('customerName1', True),
    ('custom_name!', False),
    ('', False),
    ('a' * 21, False),
    ('a a', False),
    ('0]', False),

])
def test_valid_name(value, response):
    assert ContactDataField.valid_name(value) == response
