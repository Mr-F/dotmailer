import pytest

from dotmailer.campaigns import Campaign
from dotmailer.exceptions import ErrorCampaignNotFound


def test_get_by_id_valid(sample_campaign):

    response = Campaign.get_by_id(sample_campaign.id)
    assert response == sample_campaign


@pytest.mark.parametrize('id_value', [
    None, 0
])
def test_get_by_id_invalid(id_value):
    with pytest.raises(Exception):
        Campaign.get_by_id(id_value)


def test_get_by_id_unknown():
    with pytest.raises(ErrorCampaignNotFound):
        Campaign.get_by_id(12120)
