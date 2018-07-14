"""
Stocks Exchange API requests
"""

import json
import hmac
import hashlib
from requests import PreparedRequest

from pystexchapi import ORDER_STATUS
from pystexchapi.utils import make_nonce, set_not_none_dict_kwargs


__all__ = ('TickerRequest', 'PricesRequest', 'StockExchangeRequest', 'ENCODING', 'CurrenciesRequest', 'MarketsRequest',
           'MarketSummaryRequest', 'TradeHistoryRequest', 'OrderbookRequest', 'GraficPublicRequest',
           'GetAccountInfoRequest', 'GetActiveOrdersRequest', 'TradeRequest', 'CancelOrderRequest',
           'PrivateTradeHistoryRequest', 'TransactionHistoryRequest', 'GraficPrivateRequest')

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


class TickerRequest(StockExchangeRequest):
    api_method = 'ticker'


class PricesRequest(StockExchangeRequest):
    api_method = 'prices'


class CurrenciesRequest(StockExchangeRequest):
    api_method = 'currencies'


class MarketsRequest(StockExchangeRequest):
    api_method = 'markets'


class MarketSummaryRequest(StockExchangeRequest):
    api_method = 'market_summary'

    def __init__(self, currency1: str, currency2: str, **kwargs):
        url = STOCK_EXCHANGE_BASE_URL.format(method=self.api_method) + '/{}/{}'.format(currency1, currency2)
        super(MarketSummaryRequest, self).__init__(url=url, **kwargs)


class TradeHistoryRequest(StockExchangeRequest):
    api_method = 'trades'

    def __init__(self, currency1: str, currency2: str, **kwargs):
        params = {'pair': '{}_{}'.format(currency1, currency2)}
        super(TradeHistoryRequest, self).__init__(params=params, **kwargs)


class OrderbookRequest(TradeHistoryRequest):
    api_method = 'orderbook'


DEFAULT_ORDER = 'DESC'
DEFAULT_COUNT = 50
DEFAULT_INTERVAL = '1D'


class GraficPublicRequest(StockExchangeRequest):
    api_method = 'grafic_public'

    def __init__(self, currency1: str, currency2: str, order: str=DEFAULT_ORDER, count: int=DEFAULT_COUNT,
                 interval: str=DEFAULT_INTERVAL, since: str=None, end: str=None, **kwargs):
        params = {
            'pair': '{}_{}'.format(currency1, currency2),
            'interval': interval,
            'order': order,
            'count': count
        }

        set_not_none_dict_kwargs(params, since=since, end=end)

        super(GraficPublicRequest, self).__init__(params=params, **kwargs)


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


class GetAccountInfoRequest(StockExchangePrivateRequest):
    api_method = 'GetInfo'


DEFAULT_TYPE = 'ALL'
DEFAULT_OWNER = 'OWN'


class GetActiveOrdersRequest(StockExchangePrivateRequest):
    api_method = 'ActiveOrders'

    def __init__(self, _from: str=None, from_id: str=None, end_id: str=None, since: str=None, end: str=None,
                 pair: str=DEFAULT_TYPE, count: int=DEFAULT_COUNT, order: str=DEFAULT_ORDER, _type: str=DEFAULT_TYPE,
                 owner: str=DEFAULT_OWNER, **kwargs):

        if count and count > DEFAULT_COUNT:
            raise ValueError('count cannot be greater than {}. Currently: {} {}'.format(DEFAULT_COUNT, count,
                                                                                        type(count)))

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

        super(GetActiveOrdersRequest, self).__init__(request_data=request_data, **kwargs)


class TradeRequest(StockExchangePrivateRequest):
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

        super(TradeRequest, self).__init__(request_data=request_data, **kwargs)


class CancelOrderRequest(StockExchangePrivateRequest):
    api_method = 'CancelOrder'

    def __init__(self, order_id: int, **kwargs):
        request_data = {
            'order_id': order_id
        }
        super(CancelOrderRequest, self).__init__(request_data=request_data, **kwargs)


class PrivateTradeHistoryRequest(StockExchangePrivateRequest):
    api_method = 'TradeHistory'

    def __init__(self, _from: int=None, from_id: str=None, end_id: str=None, since: str=None, end: str=None,
                 pair: str='ALL', count: int=DEFAULT_COUNT, order: str=DEFAULT_ORDER, owner: str=DEFAULT_OWNER,
                 status: int=3, **kwargs):
        request_data = {
            'pair': pair,
            'from': _from,
            'count': count,
            'from_id': from_id,
            'end_id': end_id,
            'order': order,
            'since': since,
            'end': end,
            'status': status,
            'owner': owner
        }
        super(PrivateTradeHistoryRequest, self).__init__(request_data=request_data, **kwargs)


class TransactionHistoryRequest(StockExchangePrivateRequest):
    api_method = 'TransHistory'
    
    def __init__(self, currency: str=DEFAULT_TYPE, _from: int=None, count: int=DEFAULT_COUNT, from_id: int=None,
                 end_id: int=None, order: str=DEFAULT_ORDER, since: str=None, end: str=None,
                 status: int=ORDER_STATUS.FINISHED, **kwargs):

        # FIXME: similar to StockExchangeGetActiveOrdersRequest

        if count and count > DEFAULT_COUNT:
            raise ValueError('count cannot be greater than {}. Currently: {} {}'.format(DEFAULT_COUNT, count,
                                                                                        type(count)))

        request_data = {
            'currency': currency,
            'count': count,
            'order': order,
            'status': status
        }
        optional_none_params = {
            'from': _from,
            'from_id': from_id,
            'end_id': end_id,
            'since': since,
            'end': end
        }
        set_not_none_dict_kwargs(request_data, **optional_none_params)

        super(TransactionHistoryRequest, self).__init__(request_data=request_data, **kwargs)


class GraficPrivateRequest(StockExchangePrivateRequest):
    api_method = 'Grafic'

    def __init__(self, pair: str=DEFAULT_TYPE, order: str=DEFAULT_ORDER, count: int=DEFAULT_COUNT,
                 interval: str=DEFAULT_INTERVAL, page: int=1, since: str=None, end: str=None, **kwargs):

        # FIXME: similiar to GraficPublicRequest

        if count and count > 100:
            raise ValueError('count cannot be greater than {}. Currently: {} {}'.format(100, count,
                                                                                        type(count)))

        request_data = {
            'pair': pair,
            'order': order,
            'count': count,
            'interval': interval,
            'page': page
        }
        set_not_none_dict_kwargs(request_data, since=since, end=end)

        super(GraficPrivateRequest, self).__init__(request_data=request_data, **kwargs)
