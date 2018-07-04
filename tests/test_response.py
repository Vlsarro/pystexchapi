import unittest
import json
import requests

from pystexchapi.response import StockExchangeResponseParser
from tests import TICKER_RESPONSE


class TestStockExchangeResponseParser(unittest.TestCase):

    def setUp(self):
        self.valid_response = requests.Response()
        _content = TICKER_RESPONSE
        self.valid_response._content = _content
        self.valid_response.status_code = 200
        self.valid_response.encoding = 'utf-8'
        self.valid_response.json = lambda: json.loads(_content)

    def test_parse(self):
        data = StockExchangeResponseParser.parse(self.valid_response)
        self.assertTrue(data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_raise_on_error(self):
        pass  # TODO: implement
