from datetime import datetime


class InvalidRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class NotFoundException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def convert_datetime_to_iso8601(dt: datetime):
    s = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
    return s[:-7] + "{:.03f}".format(float(s[-7:]))[1:] + 'Z'
