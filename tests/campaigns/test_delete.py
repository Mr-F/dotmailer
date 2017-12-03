import pytest

from dotmailer.campaigns import Campaign
from dotmailer.exceptions import ErrorCampaignNotFound

from tests.campaigns import sample_campaign_data


def test_delete_valid(sample_campaign):
    assert sample_campaign.id is not None
    sample_campaign.delete()
    assert sample_campaign.id is None


def test_delete_invalid():
    campaign = Campaign(**sample_campaign_data())
    with pytest.raises(Exception):
        campaign.delete()

    campaign.id = 0
    with pytest.raises(Exception):
        campaign.delete()


def test_delete_unknown():
    campaign = Campaign(**sample_campaign_data())
    campaign.id = 1289
    with pytest.raises(ErrorCampaignNotFound):
        campaign.delete()
