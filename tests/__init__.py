from dotmailer.exceptions import ErrorDatafieldNotfound

def manually_delete_address_book(connection, address_book):
    if address_book.id is not None:
        # Attempt to remove the created address book
        connection.delete('/v2/address-books/{}'.format(address_book.id))


def manually_delete_contact(connection, contact):
    if contact.id is not None:
        # Attempt to remove the created contact
        connection.delete('/v2/contacts/{}'.format(contact.id))


def manually_delete_campaign(connection, campaign):
    if campaign.id is not None:
        # Attempt to remove the created campaign
        connection.delete('/v2/campaigns/{}'.format(campaign.id))

def manually_delete_contact_data_field(connection, contact_data_field):
    try:
        connection.delete('/v2/data-fields/{}'.format(contact_data_field.name))
    except ErrorDatafieldNotfound as e:
        pass
