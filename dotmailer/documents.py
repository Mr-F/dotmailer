import datetime
from dotmailer import Folder, File
from dotmailer.connection import connection


class DocumentFolder(Folder):

    end_point = '/v2/document-folders'

    def get_all_documents(self):
        self.validate_id()
        response = connection.get('{}/{}/documents'.format(self.id))
        return [Document(**entry) for entry in response]


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
        super(File, self)._update_values(data)

    def create(self, document_folder):
        if self.file_name is not None:
            raise Exception('Document has already been uploaded to DotMailer')
        return self._create(document_folder)
