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
    
    **data_fields** - `A dictionary of values which any data fields 
    and value that should be associated with the contact e.g`
    
    .. code-block:: python
        
        { 
            'FavouriteColour': 'Red', 
            'age': 23
        }
    
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
        self.unsubscribe = self._unsubscribe

        self.get_score_by_id = self._get_score_by_id

        # Setup the other optional fields to the default value if they have not
        # been specified.
        if 'opt_in_type' not in kwargs:
            kwargs['opt_in_type'] = constants.CONTACT_OPTINTYPE_UNKNOWN
        if 'email_type' not in kwargs:
            kwargs['email_type'] = constants.CONTACT_EMAILTYPE_HTML
        if 'data_fields' not in kwargs:
            kwargs['data_fields'] = None
        super(Contact, self).__init__(**kwargs)


    def _update_values(self, data):
        if 'data_fields' in data:
            # If the data fields is a list then this is likely to be
            # coming back from the server as a list of dictionaries
            # so we need to unpack them
            if isinstance(data['data_fields'], list):
                data['data_fields'] = {
                    entry['key']:entry['value']
                    for entry in data['data_fields']
                }
        super(Contact, self)._update_values(data)

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
            '{}/{}'.format(cls.end_point, id)
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

    @classmethod
    def get_all_contacts_since(cls, date, with_full_data=True):
        """
        Get all the contacts that have been created since a specific 
        date.  
        
        This function will automatically handle making all the calls
        required to get a complete list i.e. if there are more than
        1000 contacts since the specified date.
        
        :param date: 
        :param with_full_data: 
        :return: 
        """
        select = 1000
        skip = 0
        all_contacts = []

        contacts = cls.get_contacts_since(date, with_full_data, select, skip)
        num_of_entries = len(contacts)
        while num_of_entries > 0:
            all_contacts.extend(contacts)
            if num_of_entries < select:
                break

            skip += select
            contacts = cls.get_contacts_since(date, with_full_data, select, skip)
            num_of_entries = len(contacts)

        return all_contacts

    @classmethod
    def bulk_create(cls, filedata):
        """
        Bulk creates, or bulk updates, contacts.
        
        This function allows you to upload a bulk number of contacts to 
        the server.  The contact data must be in either a CSV or Excel
        format, and it must include one column that is called 'Email' or
        equivalent if your account is using a language other than 
        English.  All other columns will be mapped to your custom contact
        data fields.
        
        Currently DotMailer place a file upload limit of 10MB.  If your
        data is larger than this then you will need to split it into
        small chunks.
        
        The API will return an ID for the import, and the current status.
        You can re-query the import status later, by using the unique
        ID value.
        
        :param filedata:  Either a file or filepath which can be read from 
        :return: 
        """

        url = '{}/imports'.format(cls.end_point)

        if isinstance(filedata, file):
            files = {'file': filedata}
            result = connection.put(url, {}, files=files)
        else:
            with open(filedata, 'r') as data:
                files = {'file': filedata}
                result = connection.put(url, {}, files=files)

        return result


    # TODO: Since this uses a different end point, should we move this to the address-book class and just call into it from here?
    @classmethod
    def bulk_create_in_address_book(cls, address_book, filedata):
        """
        Bulk creates, or bulk updates, contacts in an address book.
        
        Similar to the bulk create verions, this function can be used to
        create a bulk number of contacts in one go.  However, this
        version will also automatically associate the contact with the
        address book that has been specified.  The contact data must be 
        in either a CSV or Excel format, and it must include one column 
        that is called 'Email' or equivalent if your account is using a 
        language other than English.  All other columns will be mapped 
        to your custom contact data fields.
        
        Currently DotMailer place a file upload limit of 10MB.  If your
        data is larger than this then you will need to split it into
        small chunks.
        
        The API will return an ID for the import, and the current status.
        You can re-query the import status later, by using the unique
        ID value.
        
        :param address_book: 
        :param filedata: 
        :return: 
        """

        url = '/v2/address-book/{}/contacts/imports'.format(address_book.id)

        if isinstance(filedata, file):
            files = {'file': filedata}
            result = connection.put(url, {}, files=files)
        else:
            with open(filedata, 'r') as data:
                files = {'file': filedata}
                result = connection.put(url, {}, files=files)

        return result

    @classmethod
    def get_contact_import_status(cls, id):
        """
        Gets the import status of a previously started contact import.
        
        :param id: The bulk upload ID value returned when you submitted
         a bulk upload request.  The ID is a GUID and should look similar
         to 842d81e8-c619-457f-bb77-ab6c4a17da39.
        :return: A dictionary that contains an the keys 'id' and 'status'.
        """
        return connection.get(
            '{}/imports/{}'.format(cls.end_point, id)
        )

    @classmethod
    def get_contact_import_report(cls, id):
        """
        Gets a report with statistics about what was successfully 
        imported, and what was unable to be imported.
        
        :param id: 
        :return: 
        """
        return connection.get(
            '{}/imports/{}/report'.format(cls.end_point, id)
        )

    # @classmethod
    # def get_contact_import_report(cls, id):
    #     """
    #     Gets a report with statistics about what was successfully
    #     imported, and what was unable to be imported.
    #
    #     :param id:
    #     :return:
    #     """
    #
    #     return connection.get(
    #         '{}/imports/{}/report-faults'.format(cls.end_point, id)
    #     )


    # https://developer.dotmailer.com/docs/get-contacts-from-address-book

    # https://developer.dotmailer.com/docs/get-modified-contacts-in-address-book-since-date

    # https://developer.dotmailer.com/docs/get-modified-contacts-since-date

    # https://developer.dotmailer.com/docs/get-suppressed-contacts-since-date

    # https://developer.dotmailer.com/docs/get-unsubscribed-contacts-since-date

    # https://developer.dotmailer.com/docs/get-unsubscribed-contacts-from-address-book-since-date

    # https://developer.dotmailer.com/docs/unsubscribe-contact

    def _unsubscribe(self):
        return type(self).unsubscribe(self.email)

    @classmethod
    def unsubscribe(cls, email):
        """
        Unsubscribes contact from account
        
        :param id: 
        :return: 
        """
        return connection.post(
            '{}/unsubscribe'.format(cls.end_point),
            {
                'Email': email
            }
        )

    # https://developer.dotmailer.com/docs/unsubscribe-contact-from-address-book

    def _resubscribe(self, preferred_local=None, return_url_to_use_if_challenged=None):
        return type(self).resubscribe(self.email, preferred_local, return_url_to_use_if_challenged)

    @classmethod
    def resubscribe(cls, email, preferred_local=None, return_url_to_use_if_challenged=None):
        payload = {
            'UnsubscribedContact': {
                'Email': email
            }
        }
        if preferred_local is not None:
            payload['PreferredLocale'] = preferred_local
        if return_url_to_use_if_challenged is not None:
            payload['ReturnUrlToUseIfChallenged'] = return_url_to_use_if_challenged

        return connection.post(
            '{}/resubscribe'.format(cls.end_point),
            payload
        )

    # https://developer.dotmailer.com/docs/resubscribe-contact-to-address-book

    @classmethod
    def get_scoring(cls, select, skip):
        """
        
        :param select: 
        :param skip: 
        :return: 
        """
        return connection.get(
            '{}/score/'.format(cls.end_point),
            query_params={
                'Select': select, 'Skip': skip
            }
        )

    @classmethod
    def get_all_scoring(cls):
        """
        
        :return: 
        """
        all_scoring = []
        select = 1000
        skip = 0
        scorings = cls.get_scoring(select, skip)
        num_of_entries = len(scorings)
        while num_of_entries > 0:
            all_scoring.extend(scorings)
            if num_of_entries < select:
                break
            skip += select
            scorings = cls.get_scoring(select, skip)
            num_of_entries = len(scorings)
        return all_scoring

    @classmethod
    def get_scoring_in_address_book(cls, address_book, select, skip):
        """
        Gets contact scoring for contacts within a specific address book or segment

        :param address_book:
        :param select: 
        :param skip: 
        :return: 
        """
        return connection.get(
            '/v2/address-books/{}/contacts/score/'.format(address_book.id),
            query_params={
                'Select': select, 'Skip': skip
            }
        )

    @classmethod
    def get_all_scoring_in_address_book(cls, address_book):
        all_scoring = []
        select = 1000
        skip = 0
        scorings = cls.get_scoring_in_address_book(address_book, select, skip)
        num_of_entries = len(scorings)
        while num_of_entries > 0:
            all_scoring.extend(scorings)
            if num_of_entries < select:
                break
            skip += select
            scorings = cls.get_scoring_in_address_book(address_book, select, skip)
            num_of_entries = len(scorings)
        return all_scoring

    @classmethod
    def get_scores_modified_since(cls, date, select, skip):
        return connection.get(
            '{}/score/modified-since/{}'.format(
                cls.end_point, date.strftime('%Y-%m-%d')
            ),
            query_params={
                'Select': select, 'Skip': skip
            }
        )

    @classmethod
    def get_all_scores_modified_since(cls, date):
        all_scoring = []
        select = 1000
        skip = 0
        scorings = cls.get_scores_modified_since(date, select, skip)
        num_of_entries = len(scorings)
        while num_of_entries > 0:
            all_scoring.extend(scorings)
            if num_of_entries < select:
                break
            skip += select
            scorings = cls.get_scores_modified_since(date, select, skip)
            num_of_entries = len(scorings)
        return all_scoring

    @classmethod
    def get_score_by_email(cls, email):
        """
        Gets contact scoring for a contact by email address

        :param email: 
        :return: 
        """
        return connection.get(
            '{}/{}/score'.format(cls.end_point, email)
        )

    @classmethod
    def get_score_by_id(cls, id):
        """
        Gets contact scoring for a contact by ID
        
        :param id: 
        :return: 
        """
        return connection.get(
            '{}/{}/score'.format(cls.end_point, id)
        )
