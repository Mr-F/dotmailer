from dotmailer import Folder
from dotmailer.documents import Document


class DocumentFolder(Folder):

    end_point = '/v2/document-folders'

    # Create is defined by the parent class "Folder"

    # Get all is defined by the parent class "Folder"

    def get_all_documents(self):
        """
        Gets all uploaded documents in this folder.

        :return:
        """
        self.validate_id()
        return Document.get_all(self.id)
