"""
Stocks Exchange API requests
"""

import json
import hmac
import hashlib
from requests import PreparedRequest

from pystexchapi.utils import make_nonce


__all__ = ('StockExchangeTickerRequest', 'StockExchangePricesRequest', 'StockExchangeRequest', 'ENCODING',
           'StockExchangeCurrenciesRequest', 'StockExchangeMarketsRequest', 'StockExchangeMarketSummaryRequest',
           'StockExchangeTradeHistoryRequest', 'StockExchangeOrderbookRequest', 'StockExchangeGraficPublicRequest',
           'StockExchangeGetAccountInfoRequest')

ENCODING = 'utf-8'
STOCK_EXCHANGE_BASE_URL = 'https://app.stocks.exchange/api2/{method}'


class StockExchangeRequest(PreparedRequest):
    available_params = ('method', 'url', 'headers', 'file', 'data', 'params', 'auth', 'cookies', 'hooks', 'json')
    api_method = None
    is_private = False

    def __init__(self, **kwargs):
        super(StockExchangeRequest, self).__init__()
        default_request_params = self._default_request_params()
        default_request_params.update(kwargs)
        params = self._sanitize_params(default_request_params)
        self.prepare(**params)

    @staticmethod
    def _default_request_headers() -> dict:
        return {
            'Content-Type': 'application/json',
            'User-Agent': 'pystexchapi'
        }

    def _default_request_params(self) -> dict:
        """
        Construct default parameters for request to Stocks Exchange API
        """
        _params = {
            'method': 'GET',
            'headers': self._default_request_headers(),
            'url': STOCK_EXCHANGE_BASE_URL.format(method=self.api_method)
        }
        return _params

    def _sanitize_params(self, params: dict) -> dict:
        """Request parameters cleaning before preparing request"""
        return {k: v for k, v in params.items() if k in self.available_params}


###################################################################
# Requests for public methods
###################################################################


class StockExchangeTickerRequest(StockExchangeRequest):
    api_method = 'ticker'


class StockExchangePricesRequest(StockExchangeRequest):
    api_method = 'prices'


class StockExchangeCurrenciesRequest(StockExchangeRequest):
    api_method = 'currencies'


class StockExchangeMarketsRequest(StockExchangeRequest):
    api_method = 'markets'


class StockExchangeMarketSummaryRequest(StockExchangeRequest):
    api_method = 'market_summary'

    def __init__(self, currency1: str, currency2: str, **kwargs):
        url = STOCK_EXCHANGE_BASE_URL.format(method=self.api_method) + '/{}/{}'.format(currency1, currency2)
        super(StockExchangeMarketSummaryRequest, self).__init__(url=url, **kwargs)


class StockExchangeTradeHistoryRequest(StockExchangeRequest):
    api_method = 'trades'

    def __init__(self, currency1: str, currency2: str, **kwargs):
        params = {'pair': '{}_{}'.format(currency1, currency2)}
        super(StockExchangeTradeHistoryRequest, self).__init__(params=params, **kwargs)


class StockExchangeOrderbookRequest(StockExchangeTradeHistoryRequest):
    api_method = 'orderbook'


class StockExchangeGraficPublicRequest(StockExchangeTradeHistoryRequest):
    api_method = 'grafic_public'

    def __init__(self, currency1: str, currency2: str, interval: str, order: str, count: int, **kwargs):
        params = {
            'pair': '{}_{}'.format(currency1, currency2),
            'interval': interval,
            'order': order,
            'count': count
        }
        super(StockExchangeGraficPublicRequest, self).__init__(params=params, **kwargs)


###################################################################
# Requests for private methods
###################################################################


class StockExchangePrivateRequest(StockExchangeRequest):

    is_private = True

    def __init__(self, api_key: str, api_secret: str, **kwargs):
        _params = self.hmac_auth(api_key, api_secret)
        kwargs.update(_params)
        super(StockExchangePrivateRequest, self).__init__(url=STOCK_EXCHANGE_BASE_URL.format(method=''), method='POST',
                                                          **kwargs)

    def hmac_auth(self, api_key: str, api_secret: str) -> dict:
        signdata = json.dumps({
            'nonce': make_nonce(),
            'method': self.api_method
        })
        sign = hmac.new(api_secret, bytearray(signdata, encoding=ENCODING), hashlib.sha512).hexdigest()
        headers = self._default_request_headers()
        headers.update({
            'Key': api_key,
            'Sign': sign
        })
        return {
            'headers': headers,
            'data': signdata
        }


class StockExchangeGetAccountInfoRequest(StockExchangePrivateRequest):
    api_method = 'GetInfo'
