from dotmailer import Base
from dotmailer.connection import connection


class TransactionEmail(Base):
    """
    
    """

    end_point = '/v2/email'
    to_addresses = []
    cc_addresses = []
    bcc_addresses = []
    subject = None
    from_address = None
    html_content = None
    plain_text_content = None

    def __init__(self, **kwargs):
        self.required_fields = [
            'to_addresses', 'subject', 'from_address', 'html_content',
            'plain_text_content'
        ]
        super(TransactionEmail, self).__init__(**kwargs)
        self.to_addresses = self._split_addresses(self.to_addresses)
        self.cc_addresses = self._split_addresses(self.cc_addresses)
        self.bcc_addresses = self._split_addresses(self.bcc_addresses)

    def _split_addresses(self, address_data):
        if not isinstance(address_data, list):
            address_data = address_data.split(',')
        return address_data

    def param_dict(self):
        data = {
            'ToAddresses': self.to_addresses,
            'Subject': self.subject,
            'FromAddress': self.from_address,
            'HtmlContent': self.html_content,
            'PlainTextContent': self.plain_text_content
        }
        if self.cc_addresses != []:
            data['CCAddress'] = self.cc_addresses
        if self.bcc_addresses != []:
            data['BCCAddress'] = self.bcc_addresses,

        return data

    def send(self):
        print self.param_dict()
        response = connection.post(
            self.end_point,
            self.param_dict()
        )
        return response

    @classmethod
    def get_stats(cls, since_date, end_date, aggregate_by):
        """
        This operation retrieves your transactional email reporting 
        statistics (number sent, delivered, opens, clicks, ISP 
        complaints and bounces) for a specified time period.

        This time period can be set with a specific end date, or 
        statistics can be aggregated by all time, week, month or day.
        
        :param since_date: A date/datetime object which represents the
            start date for which transactional email reporting 
            statistics will be returned.
        :param end_date: A date/datetime object which represents the end
            date up to which transactional email reporting wil be 
            returned (inclusive). 
        :param aggregate_by: The data aggregation period for 
            transactional email reporting statistics
            
        :return: 
        """

        return connection.get(
            '{}/stats/since-date/{}'.format(
                cls.end_point, since_date.strftime('%Y-%m-%d')
            ),
            query_params={
                'EndDate': end_date.strftime('%Y-%m-%d'),
                'AggregatedBy': aggregate_by
            }
        )

    @classmethod
    def send_transactional_triggered_campaign(cls, to_addresses, campaign_id, personalisation_values=None):
        """
        
        :param to_addresses: A list of email addresses which the campaign should be sent to.
        :param campaign_id: The DotMailer ID value of the campaign you wish to trigger.
        :param personalisation_values: A dictionary of any personalisation values that should be used to fill in the
         email.
        :return: 
        """


        # TODO: Waiting to hear back from DotMailer to find out if you send multiple recipients how personalisation values are handled
        param_data = {
            'toAddresses': to_addresses,
            'campaignId': campaign_id
        }
        if personalisation_values is not None:
            param_data['personalizationValues'] = [
                {'Name': key, 'Value': value} for key, value in personalisation_values.items()
            ]

        return connection.post(
            '{}/triggered-campaign'.format(cls.end_point),
            param_data
        )

