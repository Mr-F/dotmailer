from constants import constants
from connection import connection


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

        :param email:
        :param optin_type:
        :param email_type:
        :return:
        """
        payload = {
            'Email': email,
            'OptInType': optin_type,
            'EmailType': email_type,
            # TODO: Add support for data fields
        }
        response = connection.post(cls.end_point, payload)
        return cls(response['email'], **response)

    def delete(self):
        pass

    # update

    def add_to_address_book(self, address_book):
        address_book.add_contact(self)

    def remove_from_address_book(self, address_book):
        address_book.delete_contact(self)

    @classmethod
    def get_by_email(cls, email):
        response = connection.get(
            cls.end_point + '/' + email
        )
        return cls(response['email'], **response)

    # TODO: Look at making this an alias of get_by_email
    @classmethod
    def get_by_id(cls, id):
        response = connection.get(
            cls.end_point + '/' + id
        )
        return cls(response['email'], **response)

    def get_address_books(self, select=1000, skip=0):
        # TODO: Turn this into a decorator would be a good idea
        # If this object has no id specified then raise an exception as
        # you aren't able to issue a delete for an address book which
        # doesn't exist on DotMailer
        if id is None:
            raise Exception()

        response = connection.get(
            '{}/{}/address-books'.format(
                self.end_point, self.id
            ),
            query_params={'Select': select, 'Skip': skip}
        )

    def get_all_address_books(self):
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
    def get_multiple(cls, select=1000, skip=0):
        # TODO: Add some validation in for the parameter data types
        response = connection.get(
            cls.end_point,
            query_param={'Select': select, 'Skip': skip}
        )
        return [cls(entry['email'], **entry) for entry in response]

    @classmethod
    def get_since(cls, date):
        response = connection.get(
            '{}/created-since/{}'.format(
                cls.end_point, date.strftime('%Y-%m-%d')
            )
        )
        return [cls(entry['email'], **entry) for entry in response]

    # bulk create contacts

    # bulk create contacts in address book
