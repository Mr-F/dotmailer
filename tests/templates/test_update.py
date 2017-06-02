import pytest
from dotmailer.templates import Template
from dotmailer.exceptions import ErrorTemplateInvalid


def test_create_valid_template(connection):
    """
    Test to confirm that using the API we can successful create a
    template in the user's account.

    :param connection:
    :return:
    """

    # First create a template which we can later update
    template = Template(
        name='Test',
        subject='test',
        from_name='demo@apiconnector.com',
        html_content='<div>Hello, world!<a href=\"http://$UNSUB$\" style=\"color: black;\"> Unsubscribe from this newsletter</a></div>',
        plain_text_content='Hello, world! $UNSUB$'
    )
    template.create()
    assert isinstance(template, Template), 'Template type returned'
    assert template.id is not None, 'Template has an ID value'
    template_id = template.id

    template.name = 'New name'
    template.update()

    updated_template = Template.get(template_id)
    assert updated_template.name == 'New name'
