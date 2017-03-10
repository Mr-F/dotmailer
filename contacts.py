from constants import constants
from connection import connection


class Contact(object):

    end_point = '/v2/contacts'
    email = None
    optin_type = None
    email_type = None
    data_fields = []

    def __init__(self, email, **kwargs):

        self.email = email
        self.optin_type = kwargs.get('optInType',
                                     constants.CONTACT_OPTINTYPE_UNKNOWN)
        self.email_type = kwargs.get('emailType',
                                     constants.CONTACT_EMAILTYPE_HTML)
        self.data_fields = kwargs.get('dataTypes', [])

    @classmethod
    def create(cls, email, optin_type, email_type):
        """

        :param email:
        :param optin_type:
        :param email_type:
        :return:
        """
        payload = {
            'email': email,
            'optInType': optin_type,
            'emailType': email_type
        }
        response = connection.post(cls.end_point, payload)
        return cls(response['email'], **response)


