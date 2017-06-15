import re
from dotmailer import Base
from dotmailer.constants import constants
from dotmailer.connection import connection

name_re = re.compile('[^a-zA-Z0-9_\-]')

class ContactDataField(Base):

    invalid_name_msg = 'Invalid contact data field name.  Please refer to ' \
                       'DotMailer\'s documentation about allowable names'
    end_point = '/v2/data-fields'
    name = None
    type = constants.TYPE_STRING
    visibility = constants.VISIBILITY_PRIVATE
    default_value = None

    def __init__(self, **kwargs):
        self.required_fields = ['name']

        # Setup the other optional fields to the default value if they have not
        # been specified.
        if 'type' not in kwargs:
            kwargs['type'] =  constants.TYPE_STRING
        if 'visibility' not in kwargs:
            kwargs['visibility'] = constants.VISIBILITY_PRIVATE
        if 'default_value' not in kwargs:
            kwargs['default_value'] = None

        super(ContactDataField, self).__init__(**kwargs)

    def __repr__(self):
        return '<ContactDataField name={}, type={}, visibility={}, ' \
               'default_value={}>'.format(
            self.name, self.type, self.visibility, self.default_value
        )

    def param_dict(self):
        return {
            'Name': self.name,
            'Type': self.type,
            'Visibility': self.visibility,
            'DefaultValue': self.default_value
        }

    def create(self):
        """
        Creates a contact data field within the account.
        
        This operation can be used to create a contact data field within your 
        account.  
        
        You can't create a contact data field that already exists. If you are 
        unsure which data fields currently exist, please call 
        get_contact_fields.

        The contact data field's name can only be up to 20 characters in length 
        and must consist of alphanumeric characters only, with hyphens and 
        underscores if required. The contact data field that is created will be 
        private by default. The amount of contact data fields you can create 
        will be limited by the account type you have.
        
        :return: 
        """
        if not self.valid_name(self.name):
            raise Exception(self.invalid_name_msg)

        response = connection.post(
            self.end_point,
            self.param_dict()
        )
        self._update_values(response)

    def delete(self):
        """
        Deletes a contact data field within the account.
        
        This operation can be used to delete a contact data field within your 
        account. You can't delete a reserved contact data field (FIRSTNAME, 
        LASTNAME, ADDRESS, POSTCODE, GENDER) or any that are currently in use 
        elsewhere in the system.

        This operation will return an API dependencies object. This will specify 
        the type of dependency and the ID of the dependency.
        
        :return: 
        """
        if not self.valid_name(self.name):
            raise Exception(self.invalid_name_msg)

        return connection.delete(
            '{}/{}'.format(self.end_point, self.name)
        )

    @classmethod
    def get_contact_fields(cls):
        """
        Lists all contact data fields within the account

        This operation returns a list of all the contact data fields within your 
        account.
        
        :return: 
        """
        response = connection.get(
            cls.end_point
        )
        custom_data_fields = []
        for entry in response:
            custom_data_fields.append(
                cls(**entry)
            )
        return custom_data_fields

    @staticmethod
    def valid_name(value):
        """
        The name of the contact data field being created, can only be up to 20 
        characters in length and must consist of alphnumeric characters only, 
        with hyphens and underscores if required.
        
        :param value: 
        :return: 
        """
        # Check that the name does not exceed the maximum length allowed by
        # dotmailer.
        if len(value) > 20:
            return False,

        # Confirm that the name only contains valid characters based upon
        # dotmailer's specification.
        if bool(name_re.search(value)):
            return False

        return True

