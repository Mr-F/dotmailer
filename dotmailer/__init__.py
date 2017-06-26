import datetime
from dotmailer.connection import connection
from dateutil.parser import parse as date_parser


def get_server_time():
    """
    Gets the UTC time as set on the server.
    
    This function returns the UTC time as set on the server so you 
    can be sure that any dateTime dependent calls that you make are 
    going to happen at the time you think they will.
    
    :return: The time on the server represented as a DateTime object
     with the correct timezone applied.
    """
    return date_parser(
        connection.get('/v2/server-time')
    )


class Base(object):

    id = None
    date_format = '%Y-%m-%dT%H:%M:%S'
    required_fields = []

    def __init__(self, **kwargs):
        """
        
        :param kwargs: 
        """
        # Always set a default value for the ID value if it hasn't been
        # specified
        if 'id' not in kwargs:
            kwargs['id'] = None

        for field in self.required_fields:
            if field not in kwargs:
                raise KeyError(
                    'You must specify {} when creating a {}'.format(
                        field, type(self).__name__)
                )
        self._update_values(kwargs)

    def _update_values(self, data):
        """

        :param data:
        :return:
        """

        if isinstance(data, dict):
            for key, value in data.items():
                setattr(self, key, value)

        elif isinstance(data, tuple):
            setattr(data[0], data[1])

    def param_dict(self):
        raise Exception()

    def validate_id(self, message='No ID value specified'):
        """
        Validates the current ID value for the object.  When calling
        this function an optional exception message can be provided,
        to provide more useful information to the caller as to the
        exception.

        :param message:
        :return:
        """
        # TODO: Add some type checking in here to help catch potential errors
        # Confirm that the object's id variable is an integer, or value
        # which can be cast to an integer value
        # TODO:

        # If this object has no ID value specified, or the value is less
        # than 1 then raise an exception with the specified message.
        if self.id is None or self.id < 1:
            raise Exception(message)

    def strftime(self, date):
        # TODO: Add some validation of the type "date" i
        return date.strftime(self.date_format)

    def strptime(self, date_string):
        if isinstance(date_string, datetime.datetime):
            return date_string

        return datetime.datetime.strptime(date_string, self.date_format)


class Folder(Base):

    parent_id = None
    name = None
    child_folder = None

    def __init__(self, **kwargs):
        self.required_fields = ['name', 'parent_id']
        if 'parent_id' not in kwargs:
            kwargs['parent_id'] = 0
        super(Folder, self).__init__(**kwargs)

    def param_dict(self):
        return {
            'Name': self.name
        }

    def create(self):
        response = connection.post(
            '{}/{}'.format(self.end_point, self.parent_id)
        )
        self._update_values(response)

    @classmethod
    def get(cls):
        response = connection.get(
            '{}'.foramt(cls.end_point)
        )
        # TODO: Implement this bit to recursively convert all the elements and child_folders into document folder objects
        return response


class File(Base):

    name = None
    local_path = None

    def __init__(self, **kwargs):
        self.required_fields = ['name']
        super(File, self).__init__(**kwargs)

    def _create(self, folder):
        if self.local_path is None:
            raise Exception('No local path to the file')
        with open(self.local_path, 'r') as file_data:
            response = connection.post(
                self.end_point.format(folder.id),
                files={'file': file_data}
            )
            response['local_path'] = None
            return self._update_values(response)
