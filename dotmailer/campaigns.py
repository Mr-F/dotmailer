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
        self.name = kwargs['name']
        self.subject = kwargs['subject']
        self.from_name = kwargs['from_name']
        self.from_address = kwargs['from_address']
        self.html_content = kwargs['html_content']
        self.plain_text_content = kwargs.get('plain_text_content', '')
        self.reply_action = kwargs.get('reply_action',
                                       constants.REPLY_ACTION_UNSET)
        self.reply_address = kwargs.get('reply_address', None)

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
        self.update_values(response)
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
        self.update_values(response)
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

