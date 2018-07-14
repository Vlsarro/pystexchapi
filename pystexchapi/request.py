"""
Stocks Exchange API requests
"""

import json
import hmac
import hashlib
from requests import PreparedRequest

from pystexchapi.utils import make_nonce, set_not_none_dict_kwargs


__all__ = ('StockExchangeTickerRequest', 'StockExchangePricesRequest', 'StockExchangeRequest', 'ENCODING',
           'StockExchangeCurrenciesRequest', 'StockExchangeMarketsRequest', 'StockExchangeMarketSummaryRequest',
           'StockExchangeTradeHistoryRequest', 'StockExchangeOrderbookRequest', 'StockExchangeGraficPublicRequest',
           'StockExchangeGetAccountInfoRequest', 'StockExchangeGetActiveOrdersRequest', 'StockExchangeTradeRequest')

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


class StockExchangeGraficPublicRequest(StockExchangeRequest):
    api_method = 'grafic_public'

    def __init__(self, currency1: str, currency2: str, order: str='DESC', count: int=50, interval: str='1D',
                 since: str=None, end: str=None, **kwargs):
        params = {
            'pair': '{}_{}'.format(currency1, currency2),
            'interval': interval,
            'order': order,
            'count': count
        }

        if since:
            params['since'] = since

        if end:
            params['end'] = end

        super(StockExchangeGraficPublicRequest, self).__init__(params=params, **kwargs)


###################################################################
# Requests for private methods
###################################################################


class StockExchangePrivateRequest(StockExchangeRequest):

    is_private = True

    def __init__(self, api_key: str, api_secret: str, **kwargs):
        _params = self.hmac_auth(api_key, api_secret, request_data=kwargs.pop('request_data', None))
        kwargs.update(_params)
        super(StockExchangePrivateRequest, self).__init__(url=STOCK_EXCHANGE_BASE_URL.format(method=''), method='POST',
                                                          **kwargs)

    def hmac_auth(self, api_key: str, api_secret: str, request_data: dict=None) -> dict:
        _data = {
            'nonce': make_nonce(),
            'method': self.api_method
        }

        if request_data:
            _data.update(request_data)

        signdata = json.dumps(_data)
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


class StockExchangeGetActiveOrdersRequest(StockExchangePrivateRequest):
    api_method = 'ActiveOrders'

    def __init__(self, _from: str=None, from_id: str=None, end_id: str=None,
                 since: str=None, end: str=None, pair: str='ALL', count: int=50, order: str='DESC',
                 _type: str='ALL', owner: str='OWN', **kwargs):

        request_data = {
            'pair': pair,
            'count': count,
            'order': order,
            'type': _type,
            'owner': owner
        }

        optional_none_params = {
            'from': _from,
            'from_id': from_id,
            'end_id': end_id,
            'since': since,
            'end': end
        }
        set_not_none_dict_kwargs(request_data, **optional_none_params)

        super(StockExchangeGetActiveOrdersRequest, self).__init__(request_data=request_data, **kwargs)


class StockExchangeTradeRequest(StockExchangePrivateRequest):
    api_method = 'Trade'
    
    def __init__(self, _type: str, currency1: str, currency2: str, amount: float, rate: float, **kwargs):
        if amount and amount < 0:
            raise ValueError('amount must be positive float number. Currently: {} {}'.format(amount, type(amount)))

        if rate and rate < 0:
            raise ValueError('rate must be positive float number. Currently: {} {}'.format(rate, type(rate)))

        if _type and _type not in ('BUY', 'SELL'):
            raise ValueError('The parameter type can be one of "BUY" or "SELL". Currently: {} {}'.format(_type,
                             type(_type)))

        request_data = {
            'pair': '{}_{}'.format(currency1, currency2),
            'type': _type,
            'amount': amount,
            'rate': rate
        }

        super(StockExchangeTradeRequest, self).__init__(request_data=request_data, **kwargs)
