import requests
import time
import threading
import warnings

from typing import Type

from pystexchapi.exc import APINoMethodException
from pystexchapi.request import TickerRequest, PricesRequest, StockExchangeRequest, CurrenciesRequest, MarketsRequest, \
    MarketSummaryRequest, TradeHistoryRequest, OrderbookRequest, GraficPublicRequest, GetAccountInfoRequest, \
    GetActiveOrdersRequest, TradeRequest, CancelOrderRequest, PrivateTradeHistoryRequest, TransactionHistoryRequest, \
    GraficPrivateRequest, DepositRequest, WithdrawRequest, GenerateWalletsRequest, TicketRequest, GetTicketsRequest, \
    ReplyTicketRequest, ENCODING
from pystexchapi.response import StockExchangeResponseParser, APIResponse


__all__ = ('StocksExchangeAPI', 'APIMethod')


try:
    import cachecontrol
    cache_adapter = cachecontrol.CacheControlAdapter()
except ImportError:
    warnings.warn('Caching is not enabled. Install CacheControl for cache enabling', ImportWarning)
    cache_adapter = None


SAVING_TIME_KEY = 'saving_time'
ONE_MINUTE = 60.0


class APIMethod(object):

    def __init__(self, name: str, request: Type[StockExchangeRequest], parser: Type[StockExchangeResponseParser]):
        self.name = name
        self.request = request
        self.parser = parser


DEFAULT_STOCKS_EXCHANGE_API_METHODS = (

    # Public methods

    APIMethod(name='ticker', request=TickerRequest, parser=StockExchangeResponseParser),
    APIMethod(name='prices', request=PricesRequest, parser=StockExchangeResponseParser),
    APIMethod(name='currencies', request=CurrenciesRequest, parser=StockExchangeResponseParser),
    APIMethod(name='markets', request=MarketsRequest, parser=StockExchangeResponseParser),
    APIMethod(name='market_summary', request=MarketSummaryRequest, parser=StockExchangeResponseParser),
    APIMethod(name='trade_history', request=TradeHistoryRequest, parser=StockExchangeResponseParser),
    APIMethod(name='orderbook', request=OrderbookRequest, parser=StockExchangeResponseParser),
    APIMethod(name='grafic', request=GraficPublicRequest, parser=StockExchangeResponseParser),

    # Private methods

    APIMethod(name='get_account_info', request=GetAccountInfoRequest, parser=StockExchangeResponseParser),
    APIMethod(name='get_active_orders', request=GetActiveOrdersRequest, parser=StockExchangeResponseParser),
    APIMethod(name='trade', request=TradeRequest, parser=StockExchangeResponseParser),
    APIMethod(name='cancel_order', request=CancelOrderRequest, parser=StockExchangeResponseParser),
    APIMethod(name='private_trade_history', request=PrivateTradeHistoryRequest, parser=StockExchangeResponseParser),
    APIMethod(name='transactions_history', request=TransactionHistoryRequest, parser=StockExchangeResponseParser),
    APIMethod(name='private_grafic', request=GraficPrivateRequest, parser=StockExchangeResponseParser),
    APIMethod(name='deposit', request=DepositRequest, parser=StockExchangeResponseParser),
    APIMethod(name='withdraw', request=WithdrawRequest, parser=StockExchangeResponseParser),
    APIMethod(name='generate_wallets', request=GenerateWalletsRequest, parser=StockExchangeResponseParser),
    APIMethod(name='ticket', request=TicketRequest, parser=StockExchangeResponseParser),
    APIMethod(name='get_tickets', request=GetTicketsRequest, parser=StockExchangeResponseParser),
    APIMethod(name='reply_ticket', request=ReplyTicketRequest, parser=StockExchangeResponseParser),
)


class StocksExchangeAPI(object):
    """
    Base class for implementing Stocks Exchange API
    """

    def __init__(self, ssl_enabled: bool=True, api_key: str='', api_secret: str='', api_methods: dict=None):
        super(StocksExchangeAPI, self).__init__()
        self.ssl_enabled = ssl_enabled
        self._api_key = bytes(api_key, encoding=ENCODING)
        self._api_secret = bytes(api_secret, encoding=ENCODING)
        self._init_default_api_methods()
        if api_methods:
            self.update_api_methods(api_methods)

    def _init_default_api_methods(self):
        self.api_methods = {method.name: method for method in DEFAULT_STOCKS_EXCHANGE_API_METHODS}

    def update_api_methods(self, api_methods: dict):
        self.api_methods.update(api_methods)

    def _query(self, req: requests.PreparedRequest) -> requests.Response:
        sess = requests.Session()

        if cache_adapter:
            sess.mount('https://', cache_adapter)
            sess.mount('http://', cache_adapter)

        response = sess.send(req, verify=self.ssl_enabled)
        response.raise_for_status()
        return response

    def query(self, parser: Type[StockExchangeResponseParser], req: Type[StockExchangeRequest],
              **kwargs) -> APIResponse:
        _req = req(**kwargs)

        if any(k in kwargs for k in (SAVING_TIME_KEY, 'with_saving')):
            response = self._query_with_saving(parser, _req, **kwargs)
        else:
            response = parser.parse(self._query(_req))

        return response

    def _query_with_saving(self, parser: Type[StockExchangeResponseParser],
                           req: StockExchangeRequest, **kwargs) -> APIResponse:
        """
        Method enables user to save parsed response for specified time and prevents additional requests in
        this time interval. This method is convenient for ban avoidance in case of too frequent requests to API.

        Reentrant lock ensures thread safety of method.
        """
        unix_timestamp_now = time.time()

        saved_data_attr_name = '{}_data'.format(req.api_method)
        record_time_attr_name = '{}_time'.format(req.api_method)

        saving_time = kwargs.get(SAVING_TIME_KEY, ONE_MINUTE)

        with threading.RLock():
            if saving_time:
                # get saved values from previous requests if period of saving is set
                data = getattr(self, saved_data_attr_name, None)
                prev_record_time = getattr(self, record_time_attr_name, None)

                if not (data and prev_record_time and (unix_timestamp_now - prev_record_time) < saving_time):
                    data = parser.parse(self._query(req))
                    setattr(self, saved_data_attr_name, data)  # store parsed response in memory
                    setattr(self, record_time_attr_name,
                            unix_timestamp_now)  # save the recording time for response
            else:
                data = parser.parse(self._query(req))

            return data

    def call(self, method: str, **kwargs) -> APIResponse:
        _method = self.api_methods.get(method)

        if not _method:
            raise APINoMethodException(method=method)

        if _method.request.is_private:
            kwargs.update({
                'api_key': self._api_key,
                'api_secret': self._api_secret
            })

        return self.query(_method.parser, _method.request, **kwargs)

    def get_available_methods(self):
        return self.api_methods.keys()
