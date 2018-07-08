import hmac
import hashlib
import requests
import requests_mock

from unittest import TestCase
from unittest.mock import patch

from pystexchapi.api import StocksExchangeAPI
from pystexchapi.request import STOCK_EXCHANGE_BASE_URL, StockExchangeTickerRequest, ENCODING
from pystexchapi.response import StockExchangeResponseParser
from tests import TICKER_RESPONSE, PRICES_RESPONSE, MARKETS_RESPONSE, GET_ACCOUT_INFO_RESPONSE


@requests_mock.Mocker()
class TestStocksExchangeAPI(TestCase):

    def setUp(self):
        self.shared_secret = 'KW9Wixy1zj9uNyzOjFbPu7YmU4iVJ1n3lEzqVAe5byx93IwugVQdlhoN03MzZW75'
        self.api = StocksExchangeAPI(api_key='ak9uh9ezAK3w7FivoRdEnIFjBg7Ywjz4sImOpIzE',
                                     api_secret=self.shared_secret)

    def assertTicker(self, m):
        self.assertTrue(m.called)
        self.assertEqual(m.call_count, 1)

        req = m.request_history[0]
        self.assertEqual(req.method, 'GET')
        self.assertEqual(req.url, 'https://app.stocks.exchange/api2/ticker')

        req_headers = req.headers
        self.assertEqual(req_headers['User-Agent'], 'pystexchapi')
        self.assertEqual(req_headers['Content-Type'], 'application/json')

        return req

    def assertAuth(self, m):
        req = m.request_history[0]
        signdata = bytearray(req.text, encoding=ENCODING)
        sign = bytes(hmac.new(bytes(self.shared_secret, encoding=ENCODING), signdata, hashlib.sha512).hexdigest(),
                     encoding=ENCODING)
        req_sign = bytes(req.headers['Sign'], encoding=ENCODING)
        self.assertTrue(hmac.compare_digest(req_sign, sign), msg='Calculated sign: {}\n'
                                                                 'Sign in request: {}'.format(sign, req_sign))

    def test_query(self, m):
        # test with predefined ticker request
        m.register_uri('GET', STOCK_EXCHANGE_BASE_URL.format(method='ticker'), text=TICKER_RESPONSE)

        _req = StockExchangeTickerRequest()
        response = self.api._query(_req)

        self.assertTicker(m)
        self.assertIsInstance(response, requests.Response)

    def test_public_query(self, m):
        # test with predefined ticker request
        m.register_uri('GET', STOCK_EXCHANGE_BASE_URL.format(method='ticker'), text=TICKER_RESPONSE)
        data = self.api.query(StockExchangeResponseParser, StockExchangeTickerRequest)

        self.assertTicker(m)
        self.assertTrue(data)

        # test queries with saving
        with patch('time.time') as time_mock:
            time_mock.return_value = 130.0

            data = self.api.query(StockExchangeResponseParser, StockExchangeTickerRequest, with_saving=True)
            self.assertEqual(m.call_count, 2)
            self.assertTrue(data)

            time_mock.return_value = 140.0
            data = self.api.query(StockExchangeResponseParser, StockExchangeTickerRequest, saving_time=60.0)
            self.assertEqual(m.call_count, 2)  # no call because time has not passed yet
            self.assertTrue(data)

            # change threshold to 5 seconds
            data = self.api.query(StockExchangeResponseParser, StockExchangeTickerRequest, saving_time=5.0)
            self.assertEqual(m.call_count, 3)
            self.assertTrue(data)

    @patch('time.time')
    def test_public_query_with_saving(self, m, time_mock):
        # test with predefined ticker request
        m.register_uri('GET', STOCK_EXCHANGE_BASE_URL.format(method='ticker'), text=TICKER_RESPONSE)
        time_mock.return_value = 130.0

        data = self.api._query_with_saving(StockExchangeResponseParser, StockExchangeTickerRequest())
        self.assertTrue(m.called)
        self.assertEqual(m.call_count, 1)
        self.assertTrue(data)

        time_mock.return_value = 140.0
        data = self.api._query_with_saving(StockExchangeResponseParser, StockExchangeTickerRequest())
        self.assertEqual(m.call_count, 1)  # there was no call to API, use saved response
        self.assertTrue(data)

        time_mock.return_value = 189.9
        data = self.api._query_with_saving(StockExchangeResponseParser, StockExchangeTickerRequest())
        self.assertEqual(m.call_count, 1)  # there was no call to API, use saved response
        self.assertTrue(data)

        time_mock.return_value = 191.0
        data = self.api._query_with_saving(StockExchangeResponseParser, StockExchangeTickerRequest())
        self.assertEqual(m.call_count, 2)
        self.assertTrue(data)

    ######################################################
    # Test public API methods
    ######################################################

    def test_ticker(self, m):
        m.register_uri('GET', STOCK_EXCHANGE_BASE_URL.format(method='ticker'), text=TICKER_RESPONSE)
        data = self.api.ticker()

        self.assertTicker(m)

        self.assertTrue(data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_prices(self, m):
        m.register_uri('GET', STOCK_EXCHANGE_BASE_URL.format(method='prices'), text=PRICES_RESPONSE)
        data = self.api.prices()

        self.assertTrue(m.called)
        self.assertEqual(m.call_count, 1)

        req = m.request_history[0]
        self.assertEqual(req.method, 'GET')
        self.assertEqual(req.url, 'https://app.stocks.exchange/api2/prices')

        req_headers = req.headers
        self.assertEqual(req_headers['User-Agent'], 'pystexchapi')
        self.assertEqual(req_headers['Content-Type'], 'application/json')

        self.assertTrue(data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)

    def test_markets(self, m):
        m.register_uri('GET', STOCK_EXCHANGE_BASE_URL.format(method='markets'), text=MARKETS_RESPONSE)

        data = self.api.markets()
        self.assertTrue(m.called)
        self.assertEqual(m.call_count, 1)

        req = m.request_history[0]
        self.assertEqual(req.method, 'GET')
        self.assertEqual(req.url, 'https://app.stocks.exchange/api2/markets')

        req_headers = req.headers
        self.assertEqual(req_headers['User-Agent'], 'pystexchapi')
        self.assertEqual(req_headers['Content-Type'], 'application/json')

        self.assertTrue(data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    ######################################################
    # Test private API methods
    ######################################################

    def test_get_account_info(self, m):
        m.register_uri('POST', STOCK_EXCHANGE_BASE_URL.format(method=''), text=GET_ACCOUT_INFO_RESPONSE)

        result = self.api.get_account_info()

        self.assertTrue(m.called)
        self.assertEqual(m.call_count, 1)
        self.assertAuth(m)
        self.assertTrue(result)
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('success'), 1)
        self.assertIn('data', result)

        req = m.request_history[0]
        req_headers = req.headers
        self.assertEqual(req_headers['User-Agent'], 'pystexchapi')
        self.assertEqual(req_headers['Content-Type'], 'application/json')
