from dotmailer import Base
from dotmailer.connection import connection
from dotmailer.constants import constants


class CampaignSends(Base):
    campaign_id = None
    address_book_ids = None
    contact_ids = None
    send_date = None
    split_test_option = None,
    status = constants.CAMPAIGN_STATUS_UNSENT

    def __init__(self, **kwargs):
        for attr in vars(self):
            setattr(self, attr, kwargs[attr])


class Campaign(Base):
    """
    
    Required Values
    name: The name of the campaign being created
    
    subject: The email subject line of the campaign

    from_name: The from name of the campaign
    

    html_content: The HTML content of the campaign that lies between 
        the opening <body> and the closing </body> only (the <body> tags 
        themselves should not be used).
    
    plain_text_content: The plain text content of the campaign    
    
    Optional Values
    from_address: The email of an existing custom from address you
        wish to use, which needs to be included within the request body

    reply_action: The required action to be taken when a reply to the 
        campaign is sent by the recipient. Possible values for this
        attribute are 'Unset', 'WebMailForward', 'Webmail', 'Delete'

    reply_to_address: The email address that you would like replies to
        be forwarded to, which needs to be included within the request 
        body
    
    
    """

    end_point = '/v2/campaigns'
    name = None
    subject = None
    from_name = None
    from_address = None
    html_content = None
    plain_text_content = None
    reply_action = constants.REPLY_ACTION_UNSET
    reply_address = None
    status = constants.CAMPAIGN_STATUS_UNSENT

    sends = {}

    def __init__(self, **kwargs):
        self.required_fields = [
            'name', 'subject', 'from_name', 'from_address', 'html_content',
            'plain_text_content'
        ]

        # Setup the other optional fields to the default value if they have not
        # been specified.
        if 'reply_action' not in kwargs:
            kwargs['reply_action'] = constants.REPLY_ACTION_UNSET
        if 'reply_address' not in kwargs:
            kwargs['reply_address'] = None
        super(Campaign, self).__init__(**kwargs)

    def _update_values(self, data):
        """
        The campagin has an odd attribute which is the from address 
        field.  We just need to store the email address which needs to
        be pulled out and assigned
        :param data: 
        :return: 
        """
        from_address = data.pop('from_address', None)
        if from_address is not None:
            data['from_address'] = from_address['email']

        super(Campaign, self)._update_values(data)

    def param_dict(self):
        return {
            'Name': self.name,
            'Subject': self.subject,
            'FromName': self.from_name,
            'FromAddress': {
                'Email': self.from_address
            },
            'HtmlContent': self.html_content,
            'PlainTextContent': self.plain_text_content,
            'ReplyAction': self.plain_text_content,
            'ReplyToAddress': self.reply_address
        }

    def create(self):
        """
        Create a campaign

        :return:
        """

        # TODO: Confirm that if I send "null" values that campaign will still be created correctly
        response = connection.post(
            self.end_point,
            self.param_dict()
        )
        self._update_values(response)
        return self

    def update(self):
        """
        Updates a given campaign

        :return:
        """
        self.validate_id('Sorry, unable to update the campaign as no ID'
                         'value is defined')
        response = connection.put(
            '{}/{}'.format(
                self.end_point, self.id
            ),
            self.param_dict()
        )
        self._update_values(response)
        return self

    @classmethod
    def copy(cls, id):
        """
        Copies a given campaign, returning the new campaign

        :param id:
        :return:
        """
        id = int(id)
        if id < 1:
            raise Exception()

        response = connection.post(
            '{}/{}'.format(
                cls.end_point, id
            )
        )
        return cls(**response)

    def delete(self):
        """
        Deletes a campaign

        :return:
        """
        self.validate_id('Sorry, unable to delete this campaign as no ID value'
                         'is defined.')

        response = connection.delete(
            '{}/{}'.format(
                self.end_point, self.id
            )
        )
        self.id = None
        return self

    def send(self, when=None, address_book_ids=None, contact_ids=None):
        """
        Sends a specified campaign to one or more address books,
        segments or contacts, either as an immediate or scheduled send

        :param when: A date time object which should define when the
        campaign should be sent.  If None then it will be sent
        immediately.
        :param address_book_ids:
        :param contact_ids:
        :return:
        """
        self.validate_id('Unable to send campaign, as no ID is defined for the'
                         'campaign')

        # TODO: Add some validation to the when value before proceeding to use it
        payload = {}

        if address_book_ids is not None:
            payload['AddressBookIDs'] = address_book_ids
        if contact_ids is not None:
            payload['ContactIDs'] = contact_ids

        # If no possible contact address have been specified then raise
        # an exception, as the caller is trying to send a campaing to
        # no-one.
        if payload == {}:
            raise Exception

        if when is not None:
            payload['SendDate'] = self.strftime(when)

        response = connection.post(
            '{}/send'.format(
                self.end_point
            ),
            payload
        )

        send = CampaignSends(**response)
        self.sends[send.id] = send
        return self

    def send_time_optimised(self, address_book_ids=None, contact_ids=None):
        """
        Sends a specified campaign to one or more address books,
        segments or contacts at the most appropriate time based upon
        their previous opens.

        :param address_book_ids:
        :param contact_ids:
        :return:
        """
        self.validate_id('Unable to send campaign, as no ID is defined for the'
                         'campaign')

        # TODO: Add some validation to the when value before proceeding to use it
        payload = {}

        if address_book_ids is not None:
            payload['AddressBookIDs'] = address_book_ids
        if contact_ids is not None:
            payload['ContactIDs'] = contact_ids

        # If no possible contact address have been specified then raise
        # an exception, as the caller is trying to send a campaing to
        # no-one.
        if payload == {}:
            raise Exception
        response = connection.post(
            '{}/send'.format(
                self.end_point
            ),
            payload
        )

        send = CampaignSends(**response)
        self.sends[send.id] = send
        return self

