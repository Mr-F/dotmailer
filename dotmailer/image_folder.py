from dotmailer import Folder, connection


class ImageFolder(Folder):

    end_point = '/v2/image-folders'

    # Create is defined by the parent class "Folder"

    # Get all is defined by the parent class "Folder"

    @classmethod
    def get_by_id(cls, id):
        response = connection.get(
            '{}/{}'.format(cls.end_point, id)
        )

        def _recursive_convert(entity):
            folder = cls(**entity)
            child_folders = entity.get('child_folders')
            if child_folders is not None and child_folders != []:
                folder.child_folders = []
                for child in child_folders:
                    folder.child_folders.append(
                        _recursive_convert(child)
                    )
            return folder

        return _recursive_convert(response)
