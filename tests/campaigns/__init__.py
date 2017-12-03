from dotmailer.constants import constants

def sample_campaign_data(**kwargs):
    data = {
        'name': 'Test campaign',
        'subject': 'Test campaign',
        'from_name': 'PyTests',
        'from_address': {'email': 'NEEDS_TO_BE_SET'},
        'html_content': constants.UNSUB_HTML_STRING,
        'plain_text_content': constants.UNSUB_PLAIN_TEXT_STRING,
        # Reply action is optional so left blank
        # Reply address is optional so left blank
    }
    data.update(kwargs)
    return data
