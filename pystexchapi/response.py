"""
Stocks Exchange API response parsers
"""

import requests

from pystexchapi.exc import APIResponseParsingException


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
            cls.check_for_errors(data)
            return data

    @staticmethod
    def check_for_errors(data: dict):
        pass  # TODO: implement error checking according to API format
