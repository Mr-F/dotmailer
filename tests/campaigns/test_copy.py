import pytest

from dotmailer.campaigns import Campaign
from dotmailer.exceptions import ErrorCampaignInvalid

from tests import manually_delete_campaign
from tests.campaigns import sample_campaign_data


def test_copy_valid(request, connection, sample_campaign):
    copy = Campaign.copy(sample_campaign.id)

    def cleanup():
        manually_delete_campaign(connection, copy)
    request.addfinalizer(cleanup)

    assert copy.name == 'Copy of {}'.format(sample_campaign.name)
    key_to_check = [
        'subject', 'from_name', 'html_content', 'plain_text_content',
        'reply_action', 'reply_to_address', 'status'
    ]
    for key in key_to_check:
        assert getattr(copy, key) == getattr(sample_campaign, key)


def test_copy_invalid():
    campaign = Campaign(**sample_campaign_data())
    with pytest.raises(TypeError):
        Campaign.copy(campaign)

    campaign.id = 0
    with pytest.raises(Exception):
        Campaign.copy(campaign)
