from dotmailer import Base
from dotmailer.constants import constants
from dotmailer.connection import connection
from dotmailer.exceptions import ErrorEnrolmentInvalid


class ProgramEnrolment(Base):

    end_point = '/v2/programs/enrolments/'
    program_id = None
    status = None
    date_created = None
    contacts = None
    address_books = None

    def __init__(self, **kwargs):
        self.get_faults = self._get_faults
        super(ProgramEnrolment, self).__init__(**kwargs)

    def param_dict(self):
        return {
            'ProgramID': self.program_id,
            'Contacts': self.contacts,
            'AddressBooks': self.address_books
        }

    def create(self):
        """
        Creates a program enrolment
        
        :return: 
        """
        response = connection.post(
            self.end_point,
            self.param_dict()
        )
        self._update_values(response)
        return self

    def _get_faults(self):
        """
        Gets all contacts that were not successfully enrolled, by 
        enrolment ID.  To call this method simply use 
        `instance.get_faults` without the underscore.
        
        :return: 
        """
        # Before proceeding check that the instance has an enrolment ID
        # specified.  If not raise an error.
        if self.id is None:
            raise ErrorEnrolmentInvalid()

        # Since the functionality is the same, with the exception that
        # we already know the ID value call the class instance passing
        # self.id in.
        return type(self).get_faults(self.id)

    @classmethod
    def get(cls, id):
        """
        Gets a program enrolment by ID

        :param id: The ID of the enrolment.  This ID is a GUID and 
            looking something like b0ff06d6-af04-4af8-a299-51bcbad94c1c
        :return: 
        """
        response = connection.get(
            '{}/{}'.format(cls.end_point, id)
        )
        return cls(**response)

    @classmethod
    def get_finished(cls, select=1000, skip=0):
        """
        Gets program enrolments which have a finished status
        
        :param select: 
        :param skip: 
        :return: 
        """
        response = connection.get(
            '{}/{}'.format(
                cls.end_point, constants.PROGRAM_ENROLMENT_FINISHED),
            query_params={'Select': select, 'Skip': skip}
        )
        return [cls(**entry) for entry in response]

    @classmethod
    def get_processing(cls, select=1000, skip=0):
        """
        Gets program enrolments which have a processing status
        
        :param select: 
        :param skip: 
        :return: 
        """
        response = connection.get(
            '{}/{}'.format(
                cls.end_point, constants.PROGRAM_ENROLMENT_PROCESSING),
            query_params={'Select': select, 'Skip': skip}
        )
        return [cls(**entry) for entry in response]

    @classmethod
    def get_faults(cls, id):
        """
        Gets all contacts that were not successfully enrolled, by 
        enrolment ID
        
        :param id: The ID of the enrolment.  This ID is a GUID and 
            looking something like b0ff06d6-af04-4af8-a299-51bcbad94c1c
        :return: 
        """
        response = connection.get(
            '{}/{}/report-faults'.format(cls.end_point, id)
        )
        return response


