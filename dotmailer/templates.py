from dotmailer import Base
from dotmailer.connection import connection


class Template(Base):
    """
    This class represents a DotMailer template.  To be able to create a 
    template you will need to define the following required fields:
    
    name: The name of the template being created, which needs to be 
        included within the request body
        
    subject: The email subject line of the template, which needs to be 
        included within the request body
    
    from_name: The from name of the template, which needs to be 
        included within the request body
    
    html_content: The HTML content of the template, which needs to be 
        included within the request body
    
    plain_text_content: The plain text content of the template, which 
        needs to be included within the request body
    
    To access an existing template from your account, you can either 
    obtain a copy of the template by accessing it directly using it's 
    unique ID value via the `get` class method.  Alternatively if you 
    don't know the it's ID, then use the `get_all` to return a list of 
    all the templates that you currently have defined within your 
    account.
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
        This operation can be used to create a new template within your 
        account.
        
        :return: 
        """
        response = connection.post(
            self.end_point,
            self.param_dict()
        )
        self._update_values(response)
        return self

    def update(self):
        """
        Updates the template
        
        :return: 
        """
        self.validate_id('Sorry unable to update this template as no ID value '
                         'has been defined.')

        # TODO: Confirm if DotMailer have any specific validation for template names that we need to implement here

        response = connection.put(
            '{}/{}'.format(self.end_point, self.id),
            self.param_dict()
        )
        self._update_values(response)
        return self

    @classmethod
    def get(cls, id):
        """
        Gets a template by ID
        
        :param id: The ID of the template
        :return: 
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
        Gets a list of all the templates in your account.
        
        :return: 
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
