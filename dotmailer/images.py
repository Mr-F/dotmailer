from dotmailer import File


class Image(File):

    end_point = '/v2/image-folders/{}/images'
    path = None

    def __init__(self, **kwargs):
        super(Image, self).__init__(**kwargs)
        if self.path is None and self.local_path is None:
            raise Exception(
                'You need to specify the path (location on DotMailer\'s FS) or local_path (location of file on local FS')

    def create(self, image_folder):
        if self.path is not None:
            raise Exception('Image has already been uploaded to DotMailer')
        return self._create(image_folder)
