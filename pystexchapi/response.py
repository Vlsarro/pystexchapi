"""
Stocks Exchange API response parsers
"""

import requests

from .exc import APIResponseParsingException


class StockExchangeResponseParser(object):

    @classmethod
    def parse(cls, response: requests.Response) -> dict:
        """
        Base parser for stocks exchange responses
        """
        try:
            data = response.json()
        except ValueError as e:
            raise APIResponseParsingException(exc=e, response=response)
        else:
            return data
