import pytest

from dotmailer.campaigns import Campaign
from dotmailer.exceptions import ErrorCampaignInvalid

from tests.campaigns import sample_campaign_data


def test_create_valid(account_from_address):
    data = sample_campaign_data()
    data['from_address']['email'] = account_from_address
    campaign = Campaign(**data)
    assert campaign.id is None

    campaign.create()
    assert campaign.id is not None
    for key, value in data.items():
        if key != 'from_address':
            assert getattr(campaign, key) == value
    assert campaign.from_address == data['from_address']['email']


@pytest.mark.parametrize('keys_to_use, error_msg',[
    ([], 'You must specify name when creating a Campaign'),
    (['name'], 'You must specify subject when creating a Campaign'),
    (['name', 'subject'], 'You must specify from_name when creating a Campaign'),
    (['name', 'subject', 'from_name'], 'You must specify from_address when creating a Campaign'),
    (['name', 'subject', 'from_name', 'from_address'], 'You must specify html_content when creating a Campaign'),
    (['name', 'subject', 'from_name', 'from_address', 'html_content'], 'You must specify plain_text_content when creating a Campaign')
])
def test_create_required_keys(account_from_address, keys_to_use, error_msg):
    data = sample_campaign_data()
    data['from_address']['email'] = account_from_address
    data = {key: value
            for key, value in sample_campaign_data().items()
            if key in keys_to_use}

    with pytest.raises(KeyError) as e:
        Campaign(**data)
    assert e.value.message == error_msg


@pytest.mark.parametrize('campaign_data, error_msg', [
    ({'name': ''}, 'The campaign that you are attempting to create has some invalid properties. Please check the settings you are using for this campaign.'),
    ({'subject': ''}, 'The campaign that you are attempting to create has some invalid properties. Please check the settings you are using for this campaign.'),
    ({'from_name': ''}, 'The campaign that you are attempting to create has some invalid properties. Please check the settings you are using for this campaign.'),
    ({'html_content': ''}, 'The campaign that you are attempting to create has some invalid properties. Please check the settings you are using for this campaign.'),
    ({'plain_text_content': ''}, 'The campaign that you are attempting to create has some invalid properties. Please check the settings you are using for this campaign.'),
    ({'from_address': None}, 'The campaign that you are attempting to create has some invalid properties. Please check the settings you are using for this campaign.')
])
def test_create_invalid(account_from_address, campaign_data, error_msg):
    data = sample_campaign_data(**campaign_data)
    if 'from_address' not in campaign_data:
        data['from_address']['email'] = account_from_address
    campaign = Campaign(**data)

    with pytest.raises(ErrorCampaignInvalid) as e:
        campaign.create()
    assert e.value.message == error_msg
