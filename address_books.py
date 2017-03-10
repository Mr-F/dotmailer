
from constants import constants
from connection import connection

class AddressBook(object):

    end_point = '/v2/address-books'
    id = None
    name = None
    visibility = constants.ADDRESSBOOK_VISIBILITY_PRIVATE

    def __init__(self, name, **kwargs):
        self.name = name
        self.id = kwargs.get('id', None)
        self.visibility = kwargs.get(
            'visibility', constants.ADDRESSBOOK_VISIBILITY_PRIVATE)

    @classmethod
    def create(cls, name, visibility=constants.ADDRESSBOOK_VISIBILITY_PRIVATE):
        """

        :param name: The name of the address book you're creating, which
        needs to be included within the request body. It can't be an
        existing address book's name, 'Test' or 'All contacts'. There is
        a limit of 128 characters.
        :param visibility: All address books are created as 'Private' by
        default but you can set it as 'Public' upon creation should you
        wish to. This needs to be included within the request body.
        :return:
        """

        if not AddressBook.valid_name(name):
            raise Exception()

        payload = {
            'name': name,
            'visibility': visibility
        }
        response = connection.post(cls.end_point, payload)

        return cls(name, **response)

    def delete(self):
        """

        :return:
        """

        # TODO: Turn this into a decorator would be a good idea
        # If this object has no id specified then raise an exception as
        # you aren't able to issue a delete for an address book which
        # doesn't exist on DotMailer
        if id is None:
            raise Exception()

        # Attempt to issue the delete request to DotMailer to remove the
        # address book
        response = connection.delete(self.end_point + str(self.id))

        # Clear the current ID value so we can't accidently call this
        # delete call multiple times
        self.id = None

    def update(self, name, visibility=constants.ADDRESSBOOK_VISIBILITY_PRIVATE):
        """

        :param name: The name of the address book you're creating, which
        needs to be included within the request body. It can't be an
        existing address book's name, 'Test' or 'All contacts'. There is
        a limit of 128 characters.
        :param visibility: All address books are created as 'Private' by
        default but you can set it as 'Public' upon creation should you
        wish to. This needs to be included within the request body.
        :return:
        """

        # TODO: Turn this into a decorator would be a good idea
        # If this object has no id specified then raise an exception as
        # you aren't able to issue a delete for an address book which
        # doesn't exist on DotMailer
        if id is None:
            raise Exception()

        if not self.valid_name(name):
            raise Exception()

        pass

    @classmethod
    def get(cls, id):
        """

        :param id: The ID of the address book
        :return:
        """
        # Cast the ID parameter to an integer
        id = int(id)

        # Check that the ID parameter is greater than zero, if not raise
        # an exception.
        if id < 1:
            raise Exception()

        response = connection.get(
            '{}/{}'.format(cls.end_point, id)
        )
        return cls(response['name'], **response)

    @classmethod
    def get_multiple(cls, select=1000, skip=0):
        """

        :param select: The select parameter requires a number between 1
        and 1000 (0 is not a valid number). You may only select a maximum
        of 1000 results in a single request. This parameter goes within
        the URL.
        :param skip: The skip parameter should be used in tandem with the
        select parameter when wanting to iterate through a whole data set.
        If you want to select the next 1000 records you should set the
        select parameter to 1000 and the skip parameter to 1000, which will
        return records 1001 to 2000. You should continue to do this until
        0 records are returned to retrieve the whole data set. This
        parameter goes within the URL.
        :return:
        """
        # TODO: Add some validation in for the parameter data types
        response = connection.get(
            cls.end_point,
            query_params={'Select': select, 'Skip':skip}
        )
        return [ cls(entry['name'], **entry) for entry in response]

    @classmethod
    def get_private(cls, select=1000, skip=0):
        # TODO: Add some validation in for the parameter data types
        response = connection.get(
            cls.end_point + '/private',
            query_params={'Select': select, 'Skip':skip}
        )
        return [ cls(entry['name'], **entry) for entry in response]

    @classmethod
    def get_public(cls, select=1000, skip=0):
        # TODO: Add some validation in for the parameter data types
        response = connection.get(
            cls.end_point + '/public',
            query_params={'Select': select, 'Skip':skip}
        )
        return [cls(entry['name'], **entry) for entry in response]

    @classmethod
    def get_all(cls):
        all_address_books = []

        select = 1000
        skip = 0
        address_books = cls.get_multiple(select, skip)
        num_of_entries = len(address_books)
        while num_of_entries > 0:
            all_address_books.extend(address_books)

            # If there weren't enough entries then there are no more to
            # load so simply break out of the loop
            if num_of_entries < select:
                break

            # Otherwise increment the skip value and request again
            skip += select
            address_books = cls.get_multiple(select, skip)
            num_of_entries = len(address_books)

        return all_address_books

    def add_contact(self, contact):
        """
        This function allows the caller to add a contact (represented by
        a Contact object) to an existing address book.

        :param contact:
        :return:
        """

        # TODO: Turn this into a decorator would be a good idea
        # If this object has no id specified then raise an exception as
        # you aren't able to issue a delete for an address book which
        # doesn't exist on DotMailer
        if id is None:
            raise Exception()

        payload = {
            'Email': contact.email,
            'OptInType': contact.optin_type,
            'EmailType': contact.email_type,
            # TODO: Add support for data fields
        }
        connection.post(
            self.end_point + '/' + str(self.id),
            payload
        )

    def delete_contact(self, contact):
        """

        :param contact:
        :return:
        """
        # TODO: Turn this into a decorator would be a good idea
        # If this object has no id specified then raise an exception as
        # you aren't able to issue a delete for an address book which
        # doesn't exist on DotMailer
        if id is None:
            raise Exception()

        if contact.id is None:
            raise Exception()

        response = connection.delete(
            '{}/{}/contacts/{}'.format(
                self.end_point, self.id, contact.id
            )
        )
        return True

    def delete_all_contacts(self):
        # TODO: Turn this into a decorator would be a good idea
        # If this object has no id specified then raise an exception as
        # you aren't able to issue a delete for an address book which
        # doesn't exist on DotMailer
        if id is None:
            raise Exception()

        response = connection.delete(
            '{}/{}/contacts'.format(
                self.end_point, self.id
            )
        )
        return True
    @staticmethod
    def valid_name(value):
        """
        Function to help determine if the name value specified is a valid
        based upon DotMailer's specification

        :param value: The name for an address book which should be
        validated
        :return: A boolean value indicating if the value given is valid
        """

        return len(value) <= 128
