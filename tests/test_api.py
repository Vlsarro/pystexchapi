import requests
import requests_mock

from unittest import TestCase
from unittest.mock import patch

from pystexchapi.api import StocksExchangeAPI
from pystexchapi.request import STOCK_EXCHANGE_BASE_URL, StockExchangeTickerRequest
from pystexchapi.response import StockExchangeResponseParser
from tests import TICKER_RESPONSE, PRICES_RESPONSE


@requests_mock.Mocker()
class TestStocksExchangeAPI(TestCase):

    def setUp(self):
        self.api = StocksExchangeAPI()

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
        data = self.api._public_query(StockExchangeResponseParser, StockExchangeTickerRequest)

        self.assertTicker(m)
        self.assertTrue(data)

        # test queries with saving
        with patch('time.time') as time_mock:
            time_mock.return_value = 130.0

            data = self.api._public_query(StockExchangeResponseParser, StockExchangeTickerRequest, with_saving=True)
            self.assertEqual(m.call_count, 2)
            self.assertTrue(data)

            time_mock.return_value = 140.0
            data = self.api._public_query(StockExchangeResponseParser, StockExchangeTickerRequest, saving_time=60.0)
            self.assertEqual(m.call_count, 2)  # no call because time has not passed yet
            self.assertTrue(data)

            # change threshold to 5 seconds
            data = self.api._public_query(StockExchangeResponseParser, StockExchangeTickerRequest, saving_time=5.0)
            self.assertEqual(m.call_count, 3)
            self.assertTrue(data)

    @patch('time.time')
    def test_public_query_with_saving(self, m, time_mock):
        # test with predefined ticker request
        m.register_uri('GET', STOCK_EXCHANGE_BASE_URL.format(method='ticker'), text=TICKER_RESPONSE)
        time_mock.return_value = 130.0

        data = self.api._public_query_with_saving(StockExchangeResponseParser, StockExchangeTickerRequest())
        self.assertTrue(m.called)
        self.assertEqual(m.call_count, 1)
        self.assertTrue(data)

        time_mock.return_value = 140.0
        data = self.api._public_query_with_saving(StockExchangeResponseParser, StockExchangeTickerRequest())
        self.assertEqual(m.call_count, 1)  # there was no call to API, use saved response
        self.assertTrue(data)

        time_mock.return_value = 189.9
        data = self.api._public_query_with_saving(StockExchangeResponseParser, StockExchangeTickerRequest())
        self.assertEqual(m.call_count, 1)  # there was no call to API, use saved response
        self.assertTrue(data)

        time_mock.return_value = 191.0
        data = self.api._public_query_with_saving(StockExchangeResponseParser, StockExchangeTickerRequest())
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
