import dotmailer.connection as dmconnection


class Account(object):

    @classmethod
    def get_account_information(cls):
        """
        Gets a summary of information about the current status of the account

        :return:
        """
        return dmconnection.connection.get(
            '/v2/account-info'
        )

    @classmethod
    def get_custom_from_addresses(cls, select=1000, skip=0):
        """
        Gets all custom from addresses which can be used in a campaign

        :return:
        """
        return dmconnection.connection.get(
            '/v2/custom-from-addresses'
        )

    @staticmethod
    def create_connection(username='demo@apiconnector.com', password='demo'):
        dmconnection.connection = dmconnection.DotMailerConnection(
            username,
            password
        )
        return dmconnection.connection
