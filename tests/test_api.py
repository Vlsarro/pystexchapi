import hmac
import hashlib
import requests
import requests_mock

from unittest import TestCase
from unittest.mock import patch

from pystexchapi.api import StocksExchangeAPI, APIMethod
from pystexchapi.exc import APINoMethodException
from pystexchapi.request import STOCK_EXCHANGE_BASE_URL, StockExchangeTickerRequest, ENCODING, StockExchangeRequest
from pystexchapi.response import StockExchangeResponseParser
from tests import TICKER_RESPONSE, PRICES_RESPONSE, MARKETS_RESPONSE, GET_ACCOUNT_INFO_RESPONSE, CURRENCIES_RESPONSE, \
    MARKET_SUMMARY_RESPONSE, TRADE_HISTORY_RESPONSE, ORDERBOOK_RESPONSE, PUBLIC_GRAFIC_RESPONSE, \
    GET_ACTIVE_ORDERS_RESPONSE, TRADE_RESPONSE, CANCEL_ORDER_RESPONSE, PRIVATE_TRADE_HISTORY_RESPONSE


class TestStocksExchangeAPI(TestCase):

    def setUp(self):
        self.shared_secret = 'KW9Wixy1zj9uNyzOjFbPu7YmU4iVJ1n3lEzqVAe5byx93IwugVQdlhoN03MzZW75'
        self.api = StocksExchangeAPI(api_key='ak9uh9ezAK3w7FivoRdEnIFjBg7Ywjz4sImOpIzE',
                                     api_secret=self.shared_secret)

    def assertAuth(self, m):
        req = m.request_history[0]
        req_signdata = bytearray(req.text, encoding=ENCODING)
        req_sign = bytes(req.headers['Sign'], encoding=ENCODING)
        sign = bytes(hmac.new(bytes(self.shared_secret, encoding=ENCODING), req_signdata, hashlib.sha512).hexdigest(),
                     encoding=ENCODING)
        self.assertTrue(hmac.compare_digest(req_sign, sign), msg='Calculated sign: {}\n'
                                                                 'Sign in request: {}'.format(sign, req_sign))

    def assertPublicMethod(self, method_name, m):
        self.assertTrue(m.called)
        self.assertEqual(m.call_count, 1)

        req = m.request_history[0]
        self.assertEqual(req.method, 'GET')
        self.assertEqual(req.url, 'https://app.stocks.exchange/api2/{}'.format(method_name))

        req_headers = req.headers
        self.assertEqual(req_headers['User-Agent'], 'pystexchapi')
        self.assertEqual(req_headers['Content-Type'], 'application/json')

        return req

    @requests_mock.Mocker()
    def test_query(self, m):
        # test with predefined ticker request
        _method_name = 'ticker'
        m.register_uri('GET', STOCK_EXCHANGE_BASE_URL.format(method=_method_name), text=TICKER_RESPONSE)

        _req = StockExchangeTickerRequest()
        response = self.api._query(_req)

        self.assertPublicMethod(_method_name, m)
        self.assertIsInstance(response, requests.Response)

    @requests_mock.Mocker()
    def test_public_query(self, m):
        # test with predefined ticker request
        _method_name = 'ticker'
        m.register_uri('GET', STOCK_EXCHANGE_BASE_URL.format(method=_method_name), text=TICKER_RESPONSE)
        data = self.api.query(StockExchangeResponseParser, StockExchangeTickerRequest)

        self.assertPublicMethod(_method_name, m)
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

    def test_get_available_methods(self):
        available_methods = self.api.get_available_methods()
        self.assertIn('ticker', available_methods)
        self.assertIn('prices', available_methods)
        self.assertIn('currencies', available_methods)
        self.assertIn('markets', available_methods)
        self.assertIn('market_summary', available_methods)
        self.assertIn('trade_history', available_methods)
        self.assertIn('orderbook', available_methods)
        self.assertIn('grafic', available_methods)
        self.assertIn('get_account_info', available_methods)

    def test_update_methods(self):
        _method_name = 'newmethod'
        new_method = APIMethod(name=_method_name, request=StockExchangeRequest, parser=StockExchangeResponseParser)
        new_methods = {new_method.name: new_method}

        new_api = StocksExchangeAPI(api_methods=new_methods)
        self.assertIn(_method_name, new_api.get_available_methods())

        self.assertNotIn(_method_name, self.api.get_available_methods())
        self.api.update_api_methods(api_methods=new_methods)
        self.assertIn(_method_name, self.api.get_available_methods())

    def test_raise_on_absent_method(self):
        with self.assertRaises(APINoMethodException) as cm:
            self.api.call('karabas')

        self.assertEqual(cm.exception.msg, 'API does not provide <karabas> method')

    @patch('time.time')
    @requests_mock.Mocker()
    def test_public_query_with_saving(self, time_mock, m):
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

    @requests_mock.Mocker()
    def test_ticker(self, m):
        _method_name = 'ticker'
        m.register_uri('GET', STOCK_EXCHANGE_BASE_URL.format(method=_method_name), text=TICKER_RESPONSE)
        data = self.api.call(_method_name)

        self.assertPublicMethod(method_name=_method_name, m=m)

        self.assertTrue(data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    @requests_mock.Mocker()
    def test_prices(self, m):
        _method_name = 'prices'
        m.register_uri('GET', STOCK_EXCHANGE_BASE_URL.format(method=_method_name), text=PRICES_RESPONSE)
        data = self.api.call(_method_name)

        self.assertPublicMethod(_method_name, m)

        self.assertTrue(data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)

    @requests_mock.Mocker()
    def test_markets(self, m):
        _method_name = 'markets'
        m.register_uri('GET', STOCK_EXCHANGE_BASE_URL.format(method=_method_name), text=MARKETS_RESPONSE)

        data = self.api.call(_method_name)
        self.assertPublicMethod(_method_name, m)
        self.assertTrue(data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    @requests_mock.Mocker()
    def test_currencies(self, m):
        _method_name = 'currencies'
        m.register_uri('GET', STOCK_EXCHANGE_BASE_URL.format(method=_method_name), text=CURRENCIES_RESPONSE)

        data = self.api.call(_method_name)
        self.assertPublicMethod(_method_name, m)
        self.assertTrue(data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    @requests_mock.Mocker()
    def test_market_summary(self, m):
        _method_name = 'market_summary'
        _method_url = '{}/BTC/USD'.format(_method_name)
        m.register_uri('GET', STOCK_EXCHANGE_BASE_URL.format(method=_method_url),
                       text=MARKET_SUMMARY_RESPONSE)

        data = self.api.call(_method_name, currency1='BTC', currency2='USD')
        self.assertPublicMethod(_method_url, m)
        self.assertTrue(data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

        with self.assertRaises(TypeError):
            self.api.call(_method_name)  # currency1 and currency2 are required arguments for request

    @requests_mock.Mocker()
    def test_trade_history(self, m):
        _method_name = 'trade_history'
        _currency1 = 'BTC'
        _currency2 = 'NXT'
        _method_url = '{}?pair={}_{}'.format('trades', _currency1, _currency2)

        m.register_uri('GET', STOCK_EXCHANGE_BASE_URL.format(method=_method_url), text=TRADE_HISTORY_RESPONSE)

        data = self.api.call(_method_name, currency1='BTC', currency2='NXT')
        self.assertPublicMethod(_method_url, m)
        self.assertTrue(data)
        self.assertEqual(data['success'], 1)

        result = data['result']
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)

        with self.assertRaises(TypeError):
            self.api.call(_method_name)  # currency1 and currency2 are required arguments for request

    @requests_mock.Mocker()
    def test_orderbook(self, m):
        _method_name = 'orderbook'
        _currency1 = 'BTC'
        _currency2 = 'NXT'
        _method_url = '{}?pair={}_{}'.format(_method_name, _currency1, _currency2)

        m.register_uri('GET', STOCK_EXCHANGE_BASE_URL.format(method=_method_url), text=ORDERBOOK_RESPONSE)

        data = self.api.call(_method_name, currency1='BTC', currency2='NXT')
        self.assertPublicMethod(_method_url, m)
        self.assertTrue(data)
        self.assertEqual(data['success'], 1)

        result = data['result']
        self.assertIsInstance(result, dict)
        self.assertIn('buy', result)
        self.assertIn('sell', result)

        with self.assertRaises(TypeError):
            self.api.call(_method_name)  # currency1 and currency2 are required arguments for request

    @requests_mock.Mocker()
    def test_public_grafic(self, m):
        _method_name = 'grafic'
        _currency1 = 'BTC'
        _currency2 = 'NXT'
        _method_url = '{}?pair={}_{}&interval=1D&order=DESC&count=50'.format('grafic_public', _currency1, _currency2)
        m.register_uri('GET', STOCK_EXCHANGE_BASE_URL.format(method=_method_url), text=PUBLIC_GRAFIC_RESPONSE)

        data = self.api.call(_method_name, currency1='BTC', currency2='NXT')
        self.assertPublicMethod(_method_url, m)
        self.assertTrue(data)
        self.assertEqual(data['success'], 1)

        result = data['data']
        self.assertIsInstance(result, dict)

        with self.assertRaises(TypeError):
            self.api.call(_method_name)  # currency1 and currency2 are required arguments for request

    ######################################################
    # Test private API methods
    ######################################################

    def assertPrivateMethod(self, method_name, response_data, m, **request_params):
        m.register_uri('POST', STOCK_EXCHANGE_BASE_URL.format(method=''), text=response_data)

        result = self.api.call(method_name, **request_params)
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
        return req

    @requests_mock.Mocker()
    def test_get_account_info(self, m):
        self.assertPrivateMethod('get_account_info', response_data=GET_ACCOUNT_INFO_RESPONSE, m=m)

    @requests_mock.Mocker()
    def test_get_active_orders(self, m):
        self.assertPrivateMethod('get_active_orders', response_data=GET_ACTIVE_ORDERS_RESPONSE, m=m)

    @requests_mock.Mocker()
    def test_trade(self, m):
        _method_name = 'trade'
        self.assertPrivateMethod(_method_name, response_data=TRADE_RESPONSE, m=m, _type='BUY', currency1='BTC',
                                 currency2='NXT', amount=2345, rate=1)

        with self.assertRaises(ValueError):
            self.api.call(_method_name, _type='DUMP', currency1='BTC', currency2='NXT', amount=2345, rate=1)

        with self.assertRaises(ValueError):
            self.api.call(_method_name, _type='BUY', currency1='BTC', currency2='NXT', amount=-235, rate=1)

        with self.assertRaises(ValueError):
            self.api.call(_method_name, _type='BUY', currency1='BTC', currency2='NXT', amount=2345, rate=-1)

    @requests_mock.Mocker()
    def test_cancel_order(self, m):
        self.assertPrivateMethod('cancel_order', response_data=CANCEL_ORDER_RESPONSE, m=m, order_id=45)

    @requests_mock.Mocker()
    def test_private_trade_history(self, m):
        self.assertPrivateMethod('private_trade_history', response_data=PRIVATE_TRADE_HISTORY_RESPONSE, m=m)
