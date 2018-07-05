import requests
import time
import threading
import warnings

from typing import Type

from pystexchapi.request import StockExchangeTickerRequest, StockExchangePricesRequest, StockExchangeRequest, \
    StockExchangeCurrenciesRequest, StockExchangeMarketsRequest, StockExchangeMarketSummaryRequest, \
    StockExchangeTradeHistoryRequest, StockExchangeOrderbookRequest, StockExchangeGraficPublicRequest
from pystexchapi.response import StockExchangeResponseParser


__all__ = ('StocksExchangeAPI',)


try:
    import cachecontrol
    cache_adapter = cachecontrol.CacheControlAdapter()
except ImportError:
    warnings.warn('Caching is not enabled. Install CacheControl for cache enabling', ImportWarning)
    cache_adapter = None


SAVING_TIME_KEY = 'saving_time'
ONE_MINUTE = 60.0


class StocksExchangeAPI(object):
    """
    Base class for implementing Stocks Exchange API
    """

    def __init__(self, ssl_enabled=True):
        super(StocksExchangeAPI, self).__init__()
        self.ssl_enabled = ssl_enabled

    def _query(self, req: requests.PreparedRequest) -> requests.Response:
        sess = requests.Session()

        if cache_adapter:
            sess.mount('https://', cache_adapter)
            sess.mount('http://', cache_adapter)

        response = sess.send(req, verify=self.ssl_enabled)
        response.raise_for_status()
        return response

    def _public_query(self, parser: Type[StockExchangeResponseParser], req: Type[StockExchangeRequest],
                      **kwargs) -> dict:
        _req = req(**kwargs)

        if any(k in kwargs for k in (SAVING_TIME_KEY, 'with_saving')):
            response = self._public_query_with_saving(parser, _req, **kwargs)
        else:
            response = parser.parse(self._query(_req))

        return response

    def _public_query_with_saving(self, parser: Type[StockExchangeResponseParser],
                                  req: StockExchangeRequest, **kwargs) -> dict:
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

    def ticker(self, **kwargs) -> dict:
        return self._public_query(StockExchangeResponseParser, StockExchangeTickerRequest, **kwargs)

    def prices(self, **kwargs) -> dict:
        return self._public_query(StockExchangeResponseParser, StockExchangePricesRequest, **kwargs)

    def currencies(self, **kwargs) -> dict:
        return self._public_query(StockExchangeResponseParser, StockExchangeCurrenciesRequest, **kwargs)

    def markets(self, **kwargs) -> dict:
        return self._public_query(StockExchangeResponseParser, StockExchangeMarketsRequest, **kwargs)

    def market_summary(self, **kwargs) -> dict:
        return self._public_query(StockExchangeResponseParser, StockExchangeMarketSummaryRequest, **kwargs)

    def trade_history(self, **kwargs) -> dict:
        return self._public_query(StockExchangeResponseParser, StockExchangeTradeHistoryRequest, **kwargs)

    def orderbook(self, **kwargs) -> dict:
        return self._public_query(StockExchangeResponseParser, StockExchangeOrderbookRequest, **kwargs)

    def grafic(self, **kwargs) -> dict:
        return self._public_query(StockExchangeResponseParser, StockExchangeGraficPublicRequest, **kwargs)
