from dotmailer import Base
from dotmailer.connection import connection


class Survey(Base):
    """
    
    """

    end_point = '/v2/surveys'

    def __init__(self, **kwargs):
        self.required_fields = []
        super(Survey, self).__init__(**kwargs)

    @classmethod
    def get_multiple(cls, assigned_to_address_book_only=True, select=1000,
                     skip=0):

        if assigned_to_address_book_only:
            assigned_to_address_book_only = 'true'
        else:
            assigned_to_address_book_only = 'false'

        response = connection.get(
            cls.end_point,
            query_params={
                'AssignedToAddressBookOnly': assigned_to_address_book_only,
                'Select': select,
                'Skip': skip
            }
        )
        return [cls(**entry) for entry in response]

    @classmethod
    def get_all(cls, assigned_to_address_book_only=True):
        select = 1000
        skip = 0
        all_surveys = []
        surveys = cls.get_multiple(assigned_to_address_book_only, select, skip)
        num_of_entries = len(surveys)
        while num_of_entries > 0:
            all_surveys.extend(surveys)

            # If there weren't enough entries then there are no more to
            # load so simply break out of the loop
            if num_of_entries < select:
                break

            skip += select
            surveys = cls.get_multiple(assigned_to_address_book_only, select,
                                       skip)
            num_of_entries = len(surveys)
        return all_surveys

    @classmethod
    def get(cls, id):
        """
        Get a survey by it's ID value
        
        :param id: The DotMailer unique ID value for the survey 
        :return: 
        """
        # Cast the ID parameter to an integer
        id = int(id)

        # Check that the ID parameter is greater than zero, if not raise
        # an exception.
        if id < 1:
            raise Exception()

        response = connection.get(
            '{}/{}'.format(cls.end_point, id)
        )
        return cls(**response)

