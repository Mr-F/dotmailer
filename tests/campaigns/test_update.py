import pytest

from dotmailer.campaigns import Campaign
from dotmailer.constants import constants
from dotmailer.exceptions import ErrorCampaignInvalid


def test_update_valid(sample_campaign):
    new_data = {
        'name': 'new name',
        'subject': 'new subject',
        'from_name': 'new from name',
        'html_content': 'new text {}'.format(constants.UNSUB_HTML_STRING),
        'plain_text_content': 'new text {}'.format(constants.UNSUB_PLAIN_TEXT_STRING)
    }
    sample_campaign._update_values(new_data)
    sample_campaign.update()

    response = Campaign.get_by_id(sample_campaign.id)
    for key, value in new_data.items():
        assert getattr(response, key) == value


@pytest.mark.parametrize('campaign_data, error_msg', [
    ({'name': ''}, 'The campaign that you are attempting to create has some invalid properties. Please check the settings you are using for this campaign.'),
    ({'subject': ''}, 'The campaign that you are attempting to create has some invalid properties. Please check the settings you are using for this campaign.'),
    ({'from_name': ''}, 'The campaign that you are attempting to create has some invalid properties. Please check the settings you are using for this campaign.'),
    ({'html_content': ''}, 'The campaign that you are attempting to create has some invalid properties. Please check the settings you are using for this campaign.'),
    ({'plain_text_content': ''}, 'The campaign that you are attempting to create has some invalid properties. Please check the settings you are using for this campaign.')
])
def test_update_invalid(sample_campaign, campaign_data, error_msg):
    sample_campaign._update_values(campaign_data)
    with pytest.raises(ErrorCampaignInvalid) as e:
        sample_campaign.update()
    assert e.value.message == error_msg
