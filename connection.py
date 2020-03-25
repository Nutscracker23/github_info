import os
import time
from http.client import HTTPSConnection, HTTPResponse
from urllib.parse import urlencode


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
        completed = False
        response = None

        while not completed:
            connection = self.clone()
            connection.request('GET', '{}?{}'.format(path, query), headers=self.headers)
            response = connection.getresponse()
            completed = self.check_status(response)

        return response

    def check_status(self, response: HTTPResponse) -> bool:
        status_class = response.status // 100
        result = False

        if status_class == 2:
            result = True

        if status_class == 3:
            result = self.check_status_redirection(response)

        if status_class == 4:
            result = self.check_status_client_error(response)

        if status_class == 5:
            result = self.check_status_server_error(response)
        return result

    @staticmethod
    def check_status_redirection(response: HTTPResponse) -> bool:
        # TODO: Add processing
        print('Response return {} code'.format(response.status))
        return False

    def check_status_client_error(self, response: HTTPResponse) -> bool:
        return self.check_rate_limit(response)

    @staticmethod
    def check_status_server_error(response: HTTPResponse) -> bool:
        # TODO: Add processing
        print('Response return {} code'.format(response.status))
        return False

    @staticmethod
    def check_rate_limit(response: HTTPResponse) -> bool:
        remaining_header = response.getheader('X-RateLimit-Remaining')
        result = False

        if remaining_header == 0:
            reset_header = response.getheader('X-RateLimit-Reset')
            print('X-RateLimit-Reset', reset_header)
            now = time.time()
            time.sleep(int(reset_header) - now + 1)
            result = True

        retry_after = response.getheader('retry-after')
        if retry_after:
            time.sleep(int(retry_after) + 1)
            result = True

        return result
