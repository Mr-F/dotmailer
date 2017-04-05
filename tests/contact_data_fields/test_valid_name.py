import pytest
from dotmailer.contact_data_fields import ContactDataField


@pytest.mark.parametrize('name, expected_outcome',[
    ('customName', True),
    ('custom-name', True),
    ('custom_name', True),
    ('customerName1', True),
    ('custom_name!', False)
])
def test_valid_name(name, expected_outcome):
    """
    Test to confirm that the valid name function
    :param name: 
    :param expected_outcome: 
    :return: 
    """
    assert ContactDataField.valid_name(name) == expected_outcome
