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
    test_template = Template(
        name='Test',
        subject='test',
        from_name='demo@apiconnector.com',
        html_content='<div>Hello, world!<a href=\"http://$UNSUB$\" style=\"color: black;\"> Unsubscribe from this newsletter</a></div>',
        plain_text_content='Hello, world! $UNSUB$'
    )
    template = test_template.create()

    assert isinstance(template, Template), 'Template type returned'
    assert template.id is not None, 'Template has an ID value'


@pytest.mark.parametrize('null_parameter', ['name', 'subject', 'from_name',
                                            'html_content',
                                            'plain_text_content'])
def test_create_missing_parameter(connection, null_parameter):
    """
    Test to confirm that if we try to submit a template via the API that the 
    error response from the API creates an appopriate exception.
    
    :param connection: 
    :param null_parameter: 
    :return: 
    """
    test_data = dict(
        name='Test',
        subject='test',
        from_name='demo@apiconnector.com',
        html_content='<div>Hello, world!<a href=\"http://$UNSUB$\" style=\"color: black;\"> Unsubscribe from this newsletter</a></div>',
        plain_text_content='Hello, world! $UNSUB$'
    )
    test_data[null_parameter] = None
    with pytest.raises(ErrorTemplateInvalid,
                       message='Expecting invalid template exception'):
        test_template = Template(**test_data)
        test_template.create()
