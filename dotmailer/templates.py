from dotmailer import Base
from dotmailer.connection import connection


class Template(Base):
    """
    This class represents a DotMailer template.  To be able to create a 
    template you will need to define the following required fields:
    
    **name** `The name of the template being created, which needs to be 
    included within the request body.`
        
    **subject** `The email subject line of the template, which needs to 
    be included within the request body.`
    
    **from_name** `The from name of the template, which needs to be 
    included within the request body.`
    
    **html_content** `The HTML content of the template, which needs to 
    be included within the request body.`
    
    **plain_text_content** `The plain text content of the template, 
    which needs to be included within the request body.`
    
    To access an existing template from your account, you can either 
    obtain a copy of the template by accessing it directly using it's 
    unique ID value via the :func:`get` class method.  Alternatively if 
    you don't know the it's ID, then use the :func:`get_all` to return 
    a list of  all the templates that you currently have defined within 
    your account.
    """

    end_point = '/v2/templates'
    name = None
    subject = None
    from_name = None
    html_content = None
    plain_text_content = None

    def __init__(self, **kwargs):
        self.required_fields = [
            'name', 'subject', 'from_name', 'html_content', 'plain_text_content'
        ]
        super(Template, self).__init__(**kwargs)

    def param_dict(self):
        return {
            'Name': self.name,
            'Subject': self.subject,
            'FromName': self.from_name,
            'HtmlContent': self.html_content,
            'PlainTextContent': self.plain_text_content
        }

    def create(self):
        """
        Create a new DotMailer template.
        
        This function will issue the create request to DotMailer's API,
        passing through all the information you have defined. 
        """
        response = connection.post(
            self.end_point,
            self.param_dict()
        )
        self._update_values(response)

    def update(self):
        """
        Updates the template 
        """
        self.validate_id('Sorry unable to update this template as no ID value '
                         'has been defined.')

        # TODO: Confirm if DotMailer have any specific validation for template names that we need to implement here

        response = connection.put(
            '{}/{}'.format(self.end_point, self.id),
            self.param_dict()
        )
        self._update_values(response)

    @classmethod
    def get(cls, id):
        """
        Attempt to get a specific template from DotMailer by it's ID value.
        
        If the ID specified can not be found/is not associated with your
        account then :class:`dotmailer.exceptions.ErrorTemplateNotFound`
        will be raised.
        
        :param id: The ID of the template.
        
        :return: A :class:`Template` instance, which represents the \
        DotMailer template.
        
        """
        id = int(id)

        if id < 1:
            raise Exception()

        response = connection.get(
            '{}/{}'.format(cls.end_point, id)
        )
        return cls(**response)

    @classmethod
    def get_all(cls):
        """
        Attempt to get a list of all the templates that you have associated
        with your account.
        
        This function continues to request for more templates until the 
        server doesn't return any more templates.
        
        :return: A list containing :class:`Template` objects that \
        represents all the templates that are associated with your account        
        """
        all_templates = []
        select = 1000
        skip = 0

        response = connection.get(
            cls.end_point,
            query_params={'Select': select, 'Skip': skip}
        )
        templates = [cls(**entry) for entry in response]
        num_of_templates = len(templates)

        while num_of_templates > 0:
            all_templates.extend(templates)

            if num_of_templates < select:
                break

            skip += select
            response = connection.get(
                cls.end_point,
                query_params={'Select': select, 'Skip': skip}
            )

            templates = [cls(**entry) for entry in response]
            num_of_templates = len(templates)

        return all_templates
