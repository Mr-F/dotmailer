import pytest

from dotmailer.contact_data_fields import ContactDataField
from dotmailer.constants import constants
from dotmailer.exceptions import ErrorDatafieldInvalid, ErrorNonUniqueDatafield

from tests import manually_delete_contact_data_field
from tests.contact_data_fields import sample_contact_data_field_data

def test_create_valid(request, connection):
    data_field = ContactDataField(
        name='TestDataField',
        type=constants.TYPE_STRING
    )
    data_field.create()

    def cleanup():
        manually_delete_contact_data_field(connection, data_field)
    request.addfinalizer(cleanup)


@pytest.mark.parametrize('data, error_msg', [
    ({}, 'You must specify name when creating a ContactDataField'),
    ({'name': ''}, 'You must specify type when creating a ContactDataField'),
    ({'type': ''}, 'You must specify name when creating a ContactDataField'),
])
def test_required_keys(data, error_msg):
    with pytest.raises(KeyError) as e:
        ContactDataField(**data)
    assert e.value.message == error_msg


@pytest.mark.parametrize('data, error_msg', [
    ({'name': 'ValidName', 'type': 'balsjdklsjkld'}, 'The data field is not valid. This means that there is something incorrect with the data field object you are sending to the method/operation, or you are referring to a non-existent data field. Check that your data field object is valid by checking the definition in the documentation.'),
    ({'name': 'ValidName', 'type': constants.TYPE_NUMERIC, 'default_value': 'Hello'},  'The data field is not valid. This means that there is something incorrect with the data field object you are sending to the method/operation, or you are referring to a non-existent data field. Check that your data field object is valid by checking the definition in the documentation.')
])
def test_create_invalid(data, error_msg):
    data_type = ContactDataField(**data)
    with pytest.raises(ErrorDatafieldInvalid) as e:
        data_type.create()
    assert e.value.message == error_msg


def test_create_duplicate(sample_contact_data_field):
    duplicate = ContactDataField(**sample_contact_data_field_data())
    with pytest.raises(ErrorNonUniqueDatafield):
        duplicate.create()
