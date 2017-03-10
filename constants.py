class ConstError(TypeError):
    pass

class Constants(object):

    def __init__(self):
        self.ADDRESSBOOK_VISIBILITY_PRIVATE = 'Private'
        self.ADDRESSBOOK_VISIBILITY_PUBLIC = 'Public'



    def __setattr__(self, key, value):
        if self.__dict__.has_key(key):
            raise self.ConstError, 'Can\'t rebind constant(%s)'%(key)
        self.__dict__[key] = value


constants = Constants()
