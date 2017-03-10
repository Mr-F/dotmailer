import simplejson as json

class DotMailerConnection(object):

    def __init__(self):
        pass

    def post(self, url, payload):

        payload = json.dumps(payload)

    def delete(self, url):
        pass

    def get(self, url):
        pass


connection = None
