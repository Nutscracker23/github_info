import time

from exceptions import UnauthorizedError, HTTPError


class ResponseClass(object):
    def __init__(self, response):
        self.response = response
        self.response_code = response.status

    def check_status(self):
        print(self.response_code)
        return getattr(self, 'status_{}'.format(self.response_code), self.default_check)()

    @staticmethod
    def default_check():
        raise HTTPError()

    @staticmethod
    def status_200():
        return True

    def status_401(self):
        raise UnauthorizedError()

    def status_403(self):
        remaining_header = self.response.getheader('X-RateLimit-Remaining')
        result = False

        if remaining_header == 0:
            reset_header = self.response.getheader('X-RateLimit-Reset')
            print('X-RateLimit-Reset:', reset_header)
            now = time.time()
            time.sleep(int(reset_header) - now + 1)

        retry_after = self.response.getheader('retry-after')
        if retry_after:
            print('retry-after:', retry_after)
            time.sleep(int(retry_after) + 1)

        return result
