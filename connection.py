import simplejson as json
import requests
from requests.auth import HTTPBasicAuth

class DotMailerConnection(object):

    url = 'https://r1-api.dotmailer.com'
    username = None
    password = None

    def __init__(self, username='demo@apiconnector.com', password='demo'):
        self.username = username
        self.password = password

    def post(self, url, payload):
        payload = json.dumps(payload)

    def delete(self, end_point):
        pass

    def get(self, end_point, query_params=None):
        response = requests.get(
            self.url + end_point,
            auth=HTTPBasicAuth(self.username, self.password),
            params=query_params
        )

        # TODO: Deal with handling error responses from the server

        return response


connection = None
