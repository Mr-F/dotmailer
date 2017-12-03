from dotmailer.templates import Template


def test_get_by_valid_id(sample_template):
    id = sample_template.id

    template_response = Template.get_by_id(sample_template.id)

    assert sample_template == template_response
