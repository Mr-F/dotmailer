import datetime

from dotmailer import File, connection


class Document(File):

    end_point = '/v2/document-folders/{}/documents'
    file_name = None
    file_size = None
    date_created = None
    date_modified = None

    def __init__(self, **kwargs):
        super(Document, self).__init__(**kwargs)
        if self.file_name is None and self.local_path is None:
            raise Exception('You need to specify the file_name (location on DotMailer\'s FS) or local_path (location of file on local FS')

    def _update_values(self, data):
        if 'date_created' in data and not isinstance(data['date_created'], datetime.datetime):
            data['date_created'] = self.strptime(data['date_created'])
        if 'date_modified' in data and not isinstance(data['date_modified'], datetime.datetime):
            data['date_modified'] = self.strptime(data['date_modified'])
        super(Document, self)._update_values(data)

    def create(self, document_folder):
        if self.file_name is not None:
            raise Exception('Document has already been uploaded to DotMailer')
        return self._create(document_folder)

    @classmethod
    def get_all(cls, document_folder_id):
        """
        Gets all uploaded documents in a given folder.

        :param document_folder_id: The ID of the folder
        :return:
        """
        response = connection.get(
            '{}/{}/documents'.format(cls.end_point, document_folder_id)
        )
        return [Document(**entry) for entry in response]
