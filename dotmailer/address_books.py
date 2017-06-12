from dotmailer import Base
from dotmailer.constants import constants
from dotmailer.connection import connection


class AddressBook(Base):
    """
    name: The name of the address book you're creating, which
        needs to be included within the request body. It can't be an
        existing address book's name, 'Test' or 'All contacts'. There is
        a limit of 128 characters.
        
    visibility: All address books are created as 'Private' by
        default but you can set it as 'Public' upon creation should you
        wish to. This needs to be included within the request body.
        
    """

    end_point = '/v2/address-books'
    name = None
    visibility = constants.VISIBILITY_PRIVATE

    def __init__(self, **kwargs):
        self.required_fields = ['name']

        # Reassign `delete` to reference the instance method rather
        # than the class method version.
        self.delete = self._delete
        super(AddressBook, self).__init__(**kwargs)

    def param_dict(self):
        return {
            'Name': self.name,
            'Visibility': self.visibility
        }

    def create(self):
        """
        Creates an address book.  If the current instance is associated
        with a DotMailer ID then an exception will be raised.
        
        :return: 
        """

        if not self.valid_name(self.name):
            raise Exception()

        if self.id is not None:
            raise Exception()

        response = connection.post(
            self.end_point,
            self.param_dict()
        )
        self._update_values(response)

    def update(self):
        """
        Updates an address book.  If either the name is invalid or the 
        instance doesn't have a DotMailer ID associated with it, then an
        exception will be raised.

        :return:
        """

        self.validate_id('Sorry unable to update this address book as no ID'
                         'value has been defined.')

        if not self.valid_name(self.name):
            raise Exception()

        response = connection.put(
            '{}/{}'.format(self.end_point, self.id),
            self.param_dict()
        )
        self._update_values(response)

    def _delete(self):
        """
        Deletes this address book.  When calling on an instance use 
        `instance.delete()`.

        :return:
        """

        # Validate that we should be able to perform a delete on this
        # AddressBook object based on a valid ID value being defined
        self.validate_id('Sorry unable to delete address book as no ID value'
                         'is defined for it')

        # Attempt to issue the delete request to DotMailer to remove the
        # address book
        type(self).delete(self.id)

        # Clear the current ID value so we can't accidently call this
        # delete call multiple times
        self.id = None

    @classmethod
    def delete(cls, id):
        """
        Deletes an address book by ID
        
        :param id: 
        :return: 
        """
        connection.delete(
            '{}/{}'.format(cls.end_point, id)
        )
        return True

    @classmethod
    def get(cls, id):
        """
        Gets an address book by ID

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
        return cls(**response)

    @classmethod
    def get_multiple(cls, select=1000, skip=0):
        """
        Gets all address books within the specified limits.  This function
        performs a query to return all the address books, limited by the
        select and skip values.  To easily get all the address books
        associated with the account call :func:`~AddressBook.get_all`.

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
        return [ cls(**entry) for entry in response]

    @classmethod
    def get_private(cls, select=1000, skip=0):
        """
        Gets all private address books

        :param select:
        :param skip:
        :return:
        """
        # TODO: Add some validation in for the parameter data types
        response = connection.get(
            cls.end_point + '/private',
            query_params={'Select': select, 'Skip':skip}
        )
        return [ cls(**entry) for entry in response]

    @classmethod
    def get_public(cls, select=1000, skip=0):
        """
        Gets all public address books

        :param select:
        :param skip:
        :return:
        """
        # TODO: Add some validation in for the parameter data types
        response = connection.get(
            cls.end_point + '/public',
            query_params={'Select': select, 'Skip':skip}
        )
        return [cls(**entry) for entry in response]

    @classmethod
    def get_all(cls, type='All'):
        """
        Automatically performs all the requests needed to return every
        single address book associated with your account.  This fucntion
        wraps the :get_multiple: address book function and continues to
        ask for more address books until either none are returned or the
        list returned is shorter than the number being requested.

        :param type: Either 'All', 'Private' or 'Public', depending on
        if you want every address book, all your private or all your
        public address books.
        :return:
        """
        if type == 'Private':
            address_book_function = cls.get_private
        elif type == 'Public':
            address_book_function = cls.get_public
        else:
            address_book_function = cls.get_multiple

        all_address_books = []

        select = 1000
        skip = 0
        address_books = address_book_function(select, skip)
        num_of_entries = len(address_books)
        while num_of_entries > 0:
            all_address_books.extend(address_books)

            # If there weren't enough entries then there are no more to
            # load so simply break out of the loop
            if num_of_entries < select:
                break

            # Otherwise increment the skip value and request again
            skip += select
            address_books = address_book_function(select, skip)
            num_of_entries = len(address_books)

        return all_address_books

    def add_contact(self, contact):
        """
        Adds a contact to a given address book

        :param contact:
        :return:
        """

        self.validate_id('Sorry, unable to add contact to the address book'
                         'as no ID value has been defined for the address '
                         'book.')

        connection.post(
            self.end_point + '/' + str(self.id),
            contact.param_dict()
        )

    def delete_contact(self, contact):
        """
        Deletes a contact from a given address book

        :param contact:
        :return:
        """
        self.validate_id('Sorry, unable to delete contact from this address'
                         'book, as no ID value has been defined for the '
                         'address book.')

        contact.validate_id('Sorry, unable to delete this contact from the'
                            'address book, as the contact has no ID value.')

        response = connection.delete(
            '{}/{}/contacts/{}'.format(
                self.end_point, self.id, contact.id
            )
        )

        return True

    def delete_multiple_contacts(self, id_list):
        """
        Deletes multiple contacts from an address book

        :param id_list:
        :return:
        """
        self.validate_id('Sorry, unable to delete contacts from this address'
                         'book, as no ID value has been defined for the '
                         'address book.')
        response = connection.post(
            '{}/{}/contacts/delete'.format(
                self.end_point, self.id
            ),
            id_list
        )

    def delete_all_contacts(self):
        """
        Deletes all contacts from a given address book

        :return:
        """
        self.validate_id('Sorry, unable to delete all contacts from this '
                         'address book, as no ID value has been defined for'
                         'the address book.')
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
