import pytest

from dotmailer.templates import Template


def test_update_valid_template():
    """
    Test to confirm that we can successfully update a template.

    :return:
    """
    template = Template(
        name='Update template test',
        subject='Subject',
        from_name='From name',
        html_content='<a href="http://$UNSUB$" style="color: black;"> Unsubscribe from this newsletter</a>',
        plain_text_content='$UNSUB$'
    )
    template.create()
    assert template.id is not None

    new_data = {
        'name': 'New update template test name',
        'subject': 'New subject value',
        'from_name': 'New from name',
        'html_content': 'Hello, %s' % template.html_content,
        'plain_text_content': 'Hello, %s' % template.plain_text_content
    }
    template._update_values(new_data)
    template.update()

    t = Template.get_by_id(template.id)
    for key, value in new_data.items():
        assert getattr(t, key) == value
