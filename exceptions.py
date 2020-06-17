class HTTPError(Exception):
    pass


class UnauthorizedError(HTTPError):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = '401 Unauthorized'

    def __str__(self):
        return self.message
