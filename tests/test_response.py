import unittest
import json
import requests

from pystexchapi.response import StockExchangeResponseParser, APIResponse
from pystexchapi.exc import APIDataException, APIResponseParsingException
from tests import TICKER_RESPONSE, GENERIC_ERROR_RESPONSE


def raise_value_error():
    raise ValueError()


class TestStockExchangeResponseParser(unittest.TestCase):

    @staticmethod
    def _make_response(content='', status_code=200) -> requests.Response:
        response = requests.Response()
        _content = content
        response._content = _content
        response.status_code = status_code
        response.encoding = 'utf-8'
        response.json = lambda: json.loads(_content)
        return response

    def test_parse(self):
        resp = StockExchangeResponseParser.parse(self._make_response(content=TICKER_RESPONSE))
        self.assertTrue(resp)
        self.assertIsInstance(resp, APIResponse)

        data = resp.data
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_raise_on_error(self):
        response = self._make_response(content=GENERIC_ERROR_RESPONSE)
        with self.assertRaises(APIDataException) as cm:
            StockExchangeResponseParser.parse(response)

        self.assertEqual(cm.exception.msg, 'Invalid request')

        response.json = raise_value_error

        with self.assertRaises(APIResponseParsingException):
            StockExchangeResponseParser.parse(response)
