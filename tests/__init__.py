def manually_delete_address_book(connection, address_book):
    # We need to check that the address book hasn't been removed
    # already otherwise we raise an error.  Therefore the assumption we
    # make is that if ID value is None then it's already been deleted so
    # no need to trigger a manual deletion
    if address_book.id is not None:
        # Attempt to remove the address book created in the test
        connection.delete('/v2/address-books/{}'.format(address_book.id))
