import datetime

class Base(object):

    id = None
    date_format = '%Y-%m-%dT%H:%M:%S'

    def update_values(self, data):
        """

        :param data:
        :return:
        """
        if isinstance(data, dict):
            for key, value in data.items():
                setattr(self, key, value)
        elif isinstance(data, tuple):
            setattr(data[0], data[1])

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
        return datetime.datetime.strptime(date_string, self.date_format)
