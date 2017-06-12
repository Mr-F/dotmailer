from dotmailer.connection import connection


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
    def setup_connection(username='demo@apiconnector.com', password='demo'):
        connection.username = username
        connection.password = password
        return connection
