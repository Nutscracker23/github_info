import os
from http.client import HTTPSConnection
from urllib.parse import urlencode

from utils import check_rate_limit


def parse_token():
    auth_token = os.getenv('AUTH_TOKEN')
    if not auth_token:
        raise EnvironmentError('AUTH_TOKEN not found')
    return auth_token


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

        connection = self.clone()
        connection.request('GET', '{}?{}'.format(path, query), headers=self.headers)
        response = connection.getresponse()

        if response.status == 403:
            check_rate_limit(response)
            return self.get_response(path, **kwargs)
        return response



