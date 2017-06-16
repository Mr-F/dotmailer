from dotmailer import Base
from dotmailer.connection import connection

class Segment(Base):

    end_point = '/v2/segments'
    name = None
    contacts = None
    status = None

    def __init__(self, **kwargs):
        self.required_fields = ['id', 'name', 'contacts']
        super(Segment, self).__init__(**kwargs)

    @classmethod
    def get(cls, select=1000, skip=0):
        response = connection.get(
            '{}'.format(cls.end_point),
            query_params={
                'select': select, 'skip': skip
            }
        )
        return [Segment(**entry) for entry in response]

    def refresh(self):
        response = connection.post(
            '{}/refresh/{}'.format(self.end_point, self.id)
        )
        self._update_values(response)

    def get_refresh_progress(self):
        response = connection.get(
            '{}/refresh/{}'.format(self.end_point, self.id)
        )
        self._update_values(response)
        return response['status']
