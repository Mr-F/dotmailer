import simplejson as json
import requests
from requests.auth import HTTPBasicAuth

class DotMailerConnection(object):

    url = 'https://r1-api.dotmailer.com'
    username = None
    password = None

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def _do_request(self, method, url, **kwargs):
        request_method = getattr(requests, method)
        response = request_method(
            url,
            auth=HTTPBasicAuth(self.username, self.password),
            **kwargs
        )

        # TODO: Deal with handling error responses from the server

        # Attempt to return the JSON response from the server
        try:
            return response.json()
        except ValueError as e:
            # If requests couldn't decode the JSON then just return the
            # text output from the response.
            return response.text


    def put(self, end_point, payload):
        return self._do_request(
            'put',
            self.url + end_point,
            json=payload
        )

    def post(self, end_point, payload):
        return self._do_request(
            'post',
            self.url + end_point,
            json=payload
        )

    def delete(self, end_point):
        return self._do_request(
            'delete',
            self.url + end_point,
        )

    def get(self, end_point, query_params=None):
        return self._do_request(
            'get',
            self.url + end_point,
            params=query_params
        )


connection = None
