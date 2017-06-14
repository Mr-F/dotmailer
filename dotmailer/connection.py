import simplejson as json
import requests
import re

from requests.auth import HTTPBasicAuth
from dotmailer import exceptions

class DotMailerConnection(object):
    """
    The DotMailerConnection provides a simply way to setup and call the
    various DotMailer API endpoints with.  This class defines the
    various methods GET, PUT, POST and DELETE which are used to
    communicate with DotMailer.  To create an instance, simply provide
    your DotMailer API user's username and password.

    Please remember that even if you have an active DotMailer account,
    this does not mean that your username is a valid API user.  Please
    check DotMailer's documentation about setting up an API account to
    use with this library (https://developer.dotmailer.com/docs/getting-started-with-the-api#section-setting-up-your-api-user)

    """

    url = 'https://r1-api.dotmailer.com'
    username = None
    password = None

    _first_cap_re = re.compile('(.)([A-Z][a-z]+)')
    _all_cap_re = re.compile('([a-z0-9])([A-Z])')


    # TODO: This might be better off in some support file
    def convert_camel_case_key(self, key):
        stage1 = self._first_cap_re.sub(r'\1_\2', key)
        return self._all_cap_re.sub(r'\1_\2', stage1).lower()

    def convert_camel_case_dict(self, data_dict):
        return {
            self.convert_camel_case_key(key): val for key, val in
        data_dict.items()
        }

    def _do_request(self, method, url, **kwargs):
        """
        This internal function provides the actual functionality to
        call DotMailer's actual end point.  When performing a request,
        this function will check the status code of the request
        performed.  If everything was successful, then the function
        will return either the JSON representation of the response (or
        if that is not possible the raw text.  If the response status
        code is not 200 then an appropriate exception will be raised to
        inform the caller of the reason it failed.

        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        request_method = getattr(requests, method)
        response = request_method(
            url,
            auth=HTTPBasicAuth(self.username, self.password),
            **kwargs
        )

        # The response status code was a success then process the
        # response and return to the caller
        if response.ok:

            try:
                json = response.json()

                # Next convert the CamelCase variables back to underscore
                # version to keep inline with PEP8 python, and return
                if isinstance(json, dict):
                    json = self.convert_camel_case_dict(json)
                elif isinstance(json, list):
                    json = [
                        self.convert_camel_case_dict(entry)
                        for entry in json
                    ]

                return json
            except ValueError as e:
                # If requests couldn't decode the JSON then just return
                # the text output from the response.
                return response.text

        # Else the response code was not 200 then an exception has been
        # raised and we need to pass that on.  This isn't pretty, but
        # it should do for a first pass
        if response.status_code == 401:
            exception_class_name = 'ErrorAccountInvalid'
        else:
            message = response.json()['message']

            # Currently aware of two type of error message formatting
            # which we need to parse.  These are
            #   'Address book cannot be written to via the API. ERROR_ADDRESSBOOK_NOTWRITABLE'
            #   'Error: ERROR_ADDRESSBOOK_NOT_FOUND'
            if message.startswith('Error: '):
                message = message[7:]

            exception_class_name = message[
                message.find('.')+1:
            ].strip().title().replace('_','')
            print "Message =", message
            print "Exception class =", exception_class_name
        raise getattr(exceptions, exception_class_name)()

    def put(self, end_point, payload, **kwargs):
        kwargs['json'] = payload
        return self._do_request(
            'put',
            self.url + end_point,
            **kwargs
        )

    def post(self, end_point, payload, **kwargs):
        kwargs['json'] = payload
        return self._do_request(
            'post',
            self.url + end_point,
            **kwargs
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


connection = DotMailerConnection()
