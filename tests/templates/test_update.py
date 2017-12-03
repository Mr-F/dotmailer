import pytest

from dotmailer.templates import Template


def test_update_valid_template(sample_template):
    """
    Test to confirm that we can successfully update a template.

    :return:
    """
    new_data = {
        'name': 'New update template test name',
        'subject': 'New subject value',
        'from_name': 'New from name',
        'html_content': 'Hello, %s' % sample_template.html_content,
        'plain_text_content': 'Hello, %s' % sample_template.plain_text_content
    }
    sample_template._update_values(new_data)
    sample_template.update()

    t = Template.get_by_id(sample_template.id)
    for key, value in new_data.items():
        assert getattr(t, key) == value
