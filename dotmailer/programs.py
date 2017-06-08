from dotmailer import Base
from dotmailer.connection import connection


class Program(Base):
    """
    
    """

    end_point = '/v2/programs'
    name = None
    status = None
    date_created = None

    @classmethod
    def get(cls, id):
        """
        Gets a program by ID
        
        :param id: The ID of the program
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
        Gets all programs
        
        :return: 
        """
        all_programs = []
        select = 1000
        skip = 0

        response = connection.get(
            cls.end_point,
            query_params={'Select': select, 'Skip': skip}
        )
        programs = [cls(**entry) for entry in response]
        num_of_programs = len(programs)

        while num_of_programs >0:
            all_programs.extend(programs)

            if num_of_programs < select:
                break

            skip += select
            response = connection.get(
                cls.end_point,
                query_params={'Select': select, 'Skip': skip}
            )
            programs = [cls(**entry) for entry in response]
            num_of_programs = len(programs)

        return programs
