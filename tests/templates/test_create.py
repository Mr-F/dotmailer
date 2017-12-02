import pytest

from dotmailer.exceptions import ErrorTemplateInvalid
from dotmailer.templates import Template


def test_create_valid_template():
    data = {
        'name': 'Test create template',
        'subject': 'Test creat template',
        'from_name': 'Tester',
        'html_content': '<p>Test Content</p><a href="http://$UNSUB$" style="color: black;"> Unsubscribe from this newsletter</a>',
        'plain_text_content': 'Test Content $UNSUB$'
    }

    template = Template(**data)
    assert template.id is None
    template.create()
    assert template.id is not None
    for key, value in data.items():
        assert getattr(template, key) == value


@pytest.mark.parametrize('template_data, error_msg', [
    ({}, 'You must specify name when creating a Template'),
    ({'name':''}, 'You must specify subject when creating a Template'),
    ({'name':'', 'subject':''}, 'You must specify from_name when creating a Template'),
    ({'name':'', 'subject':'', 'from_name': ''}, 'You must specify html_content when creating a Template'),
    ({'name':'', 'subject':'', 'from_name': '', 'html_content': ''}, 'You must specify plain_text_content when creating a Template'),
])
def test_create_required_keys(template_data, error_msg):
    with pytest.raises(KeyError, message=error_msg) as e:
        template = Template(**template_data)
        template.create()
    print e.__dict__
    assert e.value.message == error_msg

@pytest.mark.parametrize('template_data, error_msg', [
    ({'name': '', 'subject': '', 'from_name': '', 'html_content': '', 'plain_text_content': ''}, 'The template is not valid. This means that there is something incorrect with the template object you are sending to the method/operation. Check that your template object is valid by checking the definition in the documentation.'),
    ({'name': 'dsda', 'subject': '', 'from_name': '', 'html_content': '', 'plain_text_content': ''}, 'The template is not valid. This means that there is something incorrect with the template object you are sending to the method/operation. Check that your template object is valid by checking the definition in the documentation.'),
    ({'name': 'asdd', 'subject': 'asdsadsa', 'from_name': '', 'html_content': '', 'plain_text_content': ''}, 'The template is not valid. This means that there is something incorrect with the template object you are sending to the method/operation. Check that your template object is valid by checking the definition in the documentation.'),
    ({'name': 'asdd', 'subject': 'asdsadsa', 'from_name': 'testing', 'html_content': '', 'plain_text_content': ''}, 'The template is not valid. This means that there is something incorrect with the template object you are sending to the method/operation. Check that your template object is valid by checking the definition in the documentation.'),
    ({'name': 'asdd', 'subject': 'asdsadsa', 'from_name': 'testing',
      'html_content': 'dasdaddasdasdsa', 'plain_text_content': ''},
     'The template is not valid. This means that there is something incorrect with the template object you are sending to the method/operation. Check that your template object is valid by checking the definition in the documentation.'),
({'name': 'asdd', 'subject': 'asdsadsa', 'from_name': 'testing',
      'html_content': 'dasdaddasdasdsa', 'plain_text_content': 'dsadasjkdlasjdklasjkld'},
     'The template is not valid. This means that there is something incorrect with the template object you are sending to the method/operation. Check that your template object is valid by checking the definition in the documentation.'),
])
def test_create_invalid_template(template_data, error_msg):
    with pytest.raises(ErrorTemplateInvalid, message=error_msg) as e:
        template = Template(**template_data)
        template.create()
    print e.__dict__
    assert e.value.message == error_msg
