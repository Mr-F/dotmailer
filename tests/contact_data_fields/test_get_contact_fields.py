from dotmailer.contact_data_fields import ContactDataField


def test_get_contact_fields(sample_contact_data_field):

    response = ContactDataField.get_contact_fields()
    assert len(response) > 1

    names = []
    for entry in response:
        assert hasattr(entry, 'name')
        assert hasattr(entry, 'type')
        assert hasattr(entry, 'visibility')
        assert hasattr(entry, 'default_value')
        names.append(entry.name)
    assert sample_contact_data_field.name in names


