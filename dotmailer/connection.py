import simplejson as json
import requests
from requests.auth import HTTPBasicAuth
from dotmailer import exceptions

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

        # Attempt to return the JSON response from the server
        try:
            response_data = response.json()
        except ValueError as e:
            # If requests couldn't decode the JSON then just return the
            # text output from the response.
            response_data = response.text

        # If the response code was not 200 then an exception has been raised
        # and we need to pass that on.  This isn't pretty, but it should do
        # for a fast pass
        if response.status_code != 200:

            exception_class_name = None
            if response.status_code == 401:
                exception_class_name = 'ErrorAccountInvalid'
            else:
                print response_data
                print response_data['message']

                exception_class_name = response_data['message']
                exception_class_name = exception_class_name[
                    exception_class_name.find(':')+1:
                ].strip().title().replace('_','')

            raise getattr(exceptions, exception_class_name)()

        return response_data

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
