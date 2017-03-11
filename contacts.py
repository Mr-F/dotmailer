from constants import constants
from connection import connection
from address_books import AddressBook

class Contact(object):

    end_point = '/v2/contacts'
    id = None
    email = None
    optin_type = constants.CONTACT_OPTINTYPE_UNKNOWN
    email_type = constants.CONTACT_EMAILTYPE_HTML
    data_fields = None

    def __init__(self, email, **kwargs):

        self.email = email
        self.id = kwargs.get('id', None)
        self.optin_type = kwargs.get('optInType',
                                     constants.CONTACT_OPTINTYPE_UNKNOWN)
        self.email_type = kwargs.get('emailType',
                                     constants.CONTACT_EMAILTYPE_HTML)
        self.data_fields = kwargs.get('dataTypes', None)

    @classmethod
    def create(cls, email, optin_type, email_type):
        """
        Creates a contact

        :param email:
        :param optin_type:
        :param email_type:
        :return:
        """
        response = connection.post(
            cls.end_point,
            {
                'Email': email,
                'OptInType': optin_type,
                'EmailType': email_type,
                # TODO: Add support for data fields
            }
        )
        return cls(response['email'], **response)

    def delete(self):
        """
        Deletes a contact

        :return:
        """
        self.validate_id('Sorry, unable to delete contact as no ID value is'
                         'defined for this contact.')

        # Attempt to issue the delete request to DotMailer to remove the
        # address book
        response = connection.delete(self.end_point + str(self.id))

        # Clear the current ID value so we can't accidently call this
        # delete call multiple times
        self.id = None

    def update(self):
        """
        Updates a contact

        :return:
        """
        self.validate_id('Sorry unable to update this contact as no ID value'
                         'has been defined.')
        response = connection.put(
            '{}/{}'.format(
                self.end_point, self.id
            ),
            {
                'Email': self.email,
                'OptInType': self.optin_type,
                'EmailType': self.email_type,
                # TODO: Add support for data fields
            }
        )

    def add_to_address_book(self, address_book):
        """
        Adds a contact to a given address book

        :param address_book:
        :return:
        """
        address_book.add_contact(self)

    def delete_from_address_book(self, address_book):
        """
        Deletes a contact from a given address book

        :param address_book:
        :return:
        """
        address_book.delete_contact(self)

    @staticmethod
    def delete_multiple_from_address_book(id_list, address_book):
        """
        Deletes multiple contacts from an address book

        :param id_list:
        :param address_book:
        :return:
        """
        address_book.delete_multiple_contacts(id_list)

    @staticmethod
    def delete_all_from_address_book(address_book):
        """
        Deletes all contacts from a given address book

        :param address_book:
        :return:
        """
        address_book.delete_all_contacts()

    @classmethod
    def get_by_email(cls, email):
        """
        Gets a contact by email address

        :param email:
        :return:
        """
        response = connection.get(
            cls.end_point + '/' + email
        )
        return cls(response['email'], **response)

    @classmethod
    def get_by_id(cls, id):
        """
        Gets a contact by ID

        :param id:
        :return:
        """
        # TODO: Add some type checking in to make sure that the value supplied is actually an int
        response = connection.get(
            cls.end_point + '/' + id
        )
        return cls(response['email'], **response)

    def get_address_books(self, select=1000, skip=0):
        """
        Gets any address books that a contact is in

        :param select:
        :param skip:
        :return:
        """
        self.validate_id('Sorry, unable to get the address books that this'
                         'contact is in, due to no ID value being associated'
                         'with the contact.')

        response = connection.get(
            '{}/{}/address-books'.format(
                self.end_point, self.id
            ),
            query_params={'Select': select, 'Skip': skip}
        )
        return [AddressBook(entry['name'], **entry) for entry in response]

    def get_all_address_books(self):
        """
        Automatically performs all requests needed to return every possible
        address book that this contact is associated with.

        :return:
        """
        all_address_books = []
        select = 1000
        skip = 0
        address_books = self.get_address_books(select, skip)
        num_of_entries = len(address_books)
        while num_of_entries > 0:
            all_address_books.extend(address_books)
            if num_of_entries < select:
                break
            skip += select
            address_books = self.get_address_books(select, skip)
            num_of_entries = len(address_books)
        return all_address_books

    @classmethod
    def get_contacts(cls, select=1000, skip=0):
        """
        Gets a list of all contacts in the account

        :param select:
        :param skip:
        :return:
        """
        # TODO: Add some validation in for the parameter data types
        response = connection.get(
            cls.end_point,
            query_param={'Select': select, 'Skip': skip}
        )
        return [cls(entry['email'], **entry) for entry in response]

    # TODO: Create a wrapper function for 'get_contacts' to perform a series of calls to get all contacts

    @classmethod
    def get_contacts_since(cls, date, with_full_data=True, select=1000, skip=0):
        """
        Gets a list of created contacts after a specified date

        :param date:
        :param with_full_data:
        :param select:
        :param skip:
        :return:
        """
        response = connection.get(
            '{}/created-since/{}'.format(
                cls.end_point, date.strftime('%Y-%m-%d')
            ),
            query_param = {
                'WithFullData': with_full_data, 'Select': select, 'Skip': skip
            }
        )
        return [cls(entry['email'], **entry) for entry in response]

    # TODO: Create a wrapper function for 'get_contacts_since' to perform a series of calls to get all contacts

    # TODO: bulk create contacts

    # TODO: bulk create contacts in address book



    # TODO: This possibly refactored into a function
    def validate_id(self, message):

        # TODO: Add some type checking in here to help catch potential errors

        # If this object has no id specified then raise an exception as
        # you aren't able to issue a delete for an address book which
        # doesn't exist on DotMailer
        if self.id is None or self.id < 1:
            raise Exception(message)
