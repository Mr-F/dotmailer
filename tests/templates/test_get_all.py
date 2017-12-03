from dotmailer.templates import Template


def test_get_all(connection):
    """

    :param connection:
    :return:
    """
    templates = Template.get_all()
    for template in templates:
        assert template.id is not None
