class ConstError(TypeError):
    pass

class Constants(object):

    def __init__(self):


        self.VISIBILITY_PRIVATE = 'Private'
        self.VISIBILITY_PUBLIC = 'Public'

        self.CONTACT_OPTINTYPE_UNKNOWN = 'Unknown'
        self.CONTACT_OPTINTYPE_SINGLE = 'Single'
        self.CONTACT_OPTINTYPE_DOUBLE = 'Double'
        self.CONTACT_OPTINTYPE_VERIFIEDDOUBLE = 'VerifiedDouble'

        self.CONTACT_EMAILTYPE_PLAIN = 'PlainText'
        self.CONTACT_EMAILTYPE_HTML = 'Html'

        self.TYPE_STRING = 'String'
        self.TYPE_NUMERIC = 'Numeric'
        self.TYPE_DATE = 'Date'
        self.TYPE_BOOLEAN = 'Boolean'



    def __setattr__(self, key, value):
        if self.__dict__.has_key(key):
            raise self.ConstError, 'Can\'t rebind constant(%s)'%(key)
        self.__dict__[key] = value


constants = Constants()
