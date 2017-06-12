from dotmailer import Base
from dotmailer.constants import constants
from dotmailer.connection import connection
from dotmailer.address_books import AddressBook

class Contact(Base):
    """
    This class represents a DotMailer contact.  To be able to create a 
    contact, you must specify the email of the contact.
    
    ``Required keyword arguments``
    
    **email** - `A string containing the email address of the contact 
    that you wish to add.`
    
    ``Optional keywoard arguments``
    
    **opt_in_type** -  `A string which represents the type of optin 
    that the contact performed.  You can either specify these values 
    by hand or use the pre-defined constant values.`
            
            * :class:`Constants`.CONTACT_OPTINTYPE_UNKNOWN
            * :class:`Constants`.CONTACT_OPTINTYPE_SINGLE
            * :class:`Constants`.CONTACT_OPTINTYPE_DOUBLE
            * :class:`Constants`.CONTACT_OPTINTYPE_VERIFIEDDOUBLE
    
    **email_type** - `A string representing the type of email that the 
    contact would prefer to receive.  This can be either plain text or 
    HTML. Alternatively use the constant values.`
        
            * :class:`Constants`.CONTACT_EMAILTYPE_HTML
            * :class:`Constants`.CONTACT_EMAILTYPE_PLAIN
    
    **data_fields** - `A list of tuples which defined any data fields 
    and value that should be associated with the contact e.g`
    
    .. code-block:: python
    
        [('FavouriteColour', 'Red'), ('age': 23)]
    """

    end_point = '/v2/contacts'
    email = None
    opt_in_type = constants.CONTACT_OPTINTYPE_UNKNOWN
    email_type = constants.CONTACT_EMAILTYPE_HTML
    data_fields = None

    def __init__(self, **kwargs):
        self.required_fields = ['email']

        # Reassign `delete` to reference the instance method rather
        # than the class method version.
        self.delete = self._delete

        # Setup the other optional fields to the default value if they have not
        # been specified.
        if 'opt_in_type' not in kwargs:
            kwargs['opt_in_type'] = constants.CONTACT_OPTINTYPE_UNKNOWN
        if 'email_type' not in kwargs:
            kwargs['email_type'] = constants.CONTACT_EMAILTYPE_HTML
        if 'data_fields' not in kwargs:
            kwargs['data_fields'] = None
        super(Contact, self).__init__(**kwargs)

    def param_dict(self):
        contact_data_fields = []
        if self.data_fields is not None:
            contact_data_fields = [
                {'key': key, 'value':value}
                for key, value in self.data_fields.items()
            ]
        return {
            'Email': self.email,
            'OptInType': self.opt_in_type,
            'EmailType': self.email_type,
            'DataFields': contact_data_fields
        }

    def create(self):
        """
        Creates a contact

        :return:
        """
        response = connection.post(
            self.end_point,
            self.param_dict()
        )
        self._update_values(response)

    def update(self):
        """
        Updates an existing contact's data.  Unlike the DotMailer's API
        you currently can NOT create a contact using the update value and
        assigning an ID value of zero.  If you need to create a contact
        then please use the create method.

        :return:
        """
        self.validate_id('Sorry unable to update this contact as no ID value'
                         'has been defined.')
        response = connection.put(
            '{}/{}'.format(self.end_point, self.id),
            self.param_dict()
        )
        self._update_values(response)
        return self

    def _delete(self):
        """
        Deletes an existing contact.  When calling on an instance use 
        `instance.delete()`.

        :return:
        """
        self.validate_id('Sorry, unable to delete contact as no ID value is'
                         'defined for this contact.')

        # Attempt to issue the delete request to DotMailer to remove the
        # address book
        type(self).delete(self.id)

        # Clear the current ID value so we can't accidently call this
        # delete call multiple times
        self.id = None
        return self

    @classmethod
    def delete(cls, id):
        connection.delete(
            '{}/{}'.format(cls.end_point, id)
        )
        return True

    def add_to_address_book(self, address_book):
        """
        Adds a contact to a specific address book

        :param address_book: This should be an instance of :class:`AddressBook`
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
        return cls(**response)

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
        return cls(**response)

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
            '{}/{}/address-books'.format(self.end_point, self.id),
            query_params={'Select': select, 'Skip': skip}
        )
        return [AddressBook(**entry) for entry in response]

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
            query_params={'Select': select, 'Skip': skip}
        )
        return [cls(**entry) for entry in response]

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
        return [cls(**entry) for entry in response]

    # TODO: Create a wrapper function for 'get_contacts_since' to perform a series of calls to get all contacts

    # TODO: bulk create contacts

    # TODO: bulk create contacts in address book
