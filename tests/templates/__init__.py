def sample_template_data(**kwargs):
    return {
        'name': 'Template name',
        'subject': 'Template subject',
        'from_name': 'Template from name',
        'html_content': '<a href="http://$UNSUB$" style="color: black;">Unsub</a>',
        'plain_text_content': '$UNSUB$'
    }
