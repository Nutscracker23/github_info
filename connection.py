import os
from http.client import HTTPSConnection, HTTPResponse
from urllib.parse import urlencode

from response import ResponseClass
from utils import parse_token


class Connection(object):
    def __init__(self, host: str = 'api.github.com', enable_debug: bool = False):
        self.headers = {
            'Authorization': "token {token}".format(
                token=parse_token()
            ),
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Nutscracker-App'
        }
        self.host = host
        self.enable_debug = enable_debug

    def clone(self) -> HTTPSConnection:
        connection = HTTPSConnection(self.host)
        if self.enable_debug:
            connection.set_debuglevel(1)
        return connection

    def get_response(self, path: str = '', **kwargs):
        query_dict = {'per_page': 100, **kwargs}
        query = urlencode(query_dict)
        completed = False
        response = None

        while not completed:
            connection = self.clone()
            connection.request('GET', '{}?{}'.format(path, query), headers=self.headers)
            response = connection.getresponse()
            completed = self.check_response(response)

        return response

    @staticmethod
    def check_response(response: HTTPResponse) -> bool:
        response_class = ResponseClass(response)
        result = response_class.check_status()
        return result
