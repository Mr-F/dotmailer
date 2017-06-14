from dotmailer import Base
from dotmailer.connection import connection


class TransactionEmail(Base):
    """
    
    """

    end_point = '/v2/email'
    to_address = []
    cc_address = []
    bcc_address = []
    subject = None
    from_address = None
    html_content = None
    plain_text_content = None

    def __init__(self, **kwargs):
        self.required_fields = [
            'to_address', 'subject', 'from_address', 'html_content',
            'plain_text_content'
        ]
        super(TransactionEmail, self).__init__(**kwargs)
        self.to_address = self._split_addresses(self.to_address)
        self.cc_address = self._split_addresses(self.cc_address)
        self.bcc_address = self._split_addresses(self.bcc_address)

    def _split_addresses(self, address_data):
        if not isinstance(address_data, list):
            address_data = address_data.split(',')
        return address_data

    def param_dict(self):
        data = {
            'toAddress': ','.join(self.to_address),
            'subject': self.subject,
            'fromAddress': self.from_address,
            'htmlContent': self.html_content,
            'plainTextContent': self.plain_text_content
        }
        if self.cc_address != []:
            data['CCAddress'] = ','.join(self.cc_address)
        if self.bcc_address != []:
            data['BCCAddress'] = ','.join(self.bcc_address),

        return data

    def send(self):
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
    def send_transactional_triggered_campaign(cls, to_address, campaign_id, personalisation_values=None):
        """
        
        :param to_address: A single email address which the campaign should be sent to.
        :param campaign_id: The DotMailer ID value of the campaign you wish to trigger.
        :param personalisation_values: A dictionary of any personalisation values that should be used to fill in the
         email.
        :return: 
        """


        # TODO: Waiting to hear back from DotMailer to find out if you send multiple recipients how personalisation values are handled
        param_data = {
            'toAddress': [to_address],
            'campaignId': campaign_id
        }
        if personalisation_values is not None:
            param_data['personalisationValues'] = [
                {'Name': key, 'Value': value} for key, value in personalisation_values.items()
            ]

        return connection.post(
            '{}/triggered-campaign'.format(cls.end_point),
            param_data
        )

