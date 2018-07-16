"""
Stocks Exchange API response parsers
"""

import requests

from pystexchapi.exc import APIResponseParsingException, APIDataException


__all__ = ('APIResponse', 'StockExchangeResponseParser')


class APIResponse(object):

    def __init__(self, data, exc=None):
        self.data = data
        self.exc = exc


class StockExchangeResponseParser(object):

    @classmethod
    def parse(cls, response: requests.Response) -> APIResponse:
        """
        Base parser for stocks exchange responses
        """
        try:
            data = response.json()
        except (ValueError, TypeError) as e:
            raise APIResponseParsingException(exc=e, response=response)
        else:
            cls.check_for_errors(data)
            return APIResponse(data)

    @staticmethod
    def check_for_errors(data):
        if isinstance(data, dict) and not int(data.get('success')):
            raise APIDataException(msg=data.get('error'))
