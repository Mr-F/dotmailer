def manually_delete_address_book(connection, address_book):
    # Attempt to remove the address book created in the test
    connection.delete('/v2/address-books/{}'.format(address_book.id))
