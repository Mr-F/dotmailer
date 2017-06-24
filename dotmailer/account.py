from dotmailer.connection import connection
from dotmailer.constants import constants


class Account(object):

    @staticmethod
    def get_account_information():
        """
        Gets a summary of information about the current status of the
        account

        :return:
        """
        return connection.get(
            '/v2/account-info'
        )

    @staticmethod
    def get_custom_from_addresses(select=1000, skip=0):
        """
        Gets all custom from addresses which can be used in a campaign

        :return:
        """
        return connection.get(
            '/v2/custom-from-addresses'
        )

    @staticmethod
    def get_all_custom_from_addresses():
        all_addresses = []
        select = 1000
        skip = 0
        addresses = Account.get_custom_from_addresses(select, skip)
        num_of_address = len(addresses)
        while num_of_address > 0:
            all_addresses.extend(addresses)

            if num_of_address < select:
                break

            skip += num_of_address
            addresses = Account.get_custom_from_addresses(select, skip)
            num_of_address = len(addresses)

        return all_addresses

    @staticmethod
    def setup_connection(username='demo@apiconnector.com', password='demo',
                         endpoint=None):
        """
        
        :param username: Your DotMailer API username 
        :param password: Your DotMailer API user's password
        :param endpoint: Your regional DotMailer end point.  If not 
        specified we will attempt to determine the correct value.  If
        we can not then the library will default to use 
        `r1-api.dotmailer.com`.
        :return: 
        """
        connection.url = constants.DEFAULT_ENDPOINT
        connection.username = username
        connection.password = password
        # If the caller has specific a different end point then use that
        if endpoint is not None:
            connection.url = endpoint

        # Else attempt to determine the correct endpoint for the user
        else:
            response = Account.get_account_information()
            for property_dict in response['properties']:
                if property_dict['name'] == 'ApiEndpoint':
                    connection.url = property_dict['value']

        return connection
