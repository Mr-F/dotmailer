class ConstError(TypeError):
    pass

class Constants(object):

    def __init__(self):

        # Address book constants
        self.ADDRESSBOOK_VISIBILITY_PRIVATE = 'Private'
        self.ADDRESSBOOK_VISIBILITY_PUBLIC = 'Public'

        # Contact constants
        self.CONTACT_OPTINTYPE_UNKNOWN = 'Unknown'
        self.CONTACT_OPTINTYPE_SINGLE = 'Single'
        self.CONTACT_OPTINTYPE_DOUBLE = 'Double'
        self.CONTACT_OPTINTYPE_VERIFIEDDOUBLE = 'VerifiedDouble'

        self.CONTACT_EMAILTYPE_PLAIN = 'PlainText'
        self.CONTACT_EMAILTYPE_HTML = 'Html'



    def __setattr__(self, key, value):
        if self.__dict__.has_key(key):
            raise self.ConstError, 'Can\'t rebind constant(%s)'%(key)
        self.__dict__[key] = value


constants = Constants()
