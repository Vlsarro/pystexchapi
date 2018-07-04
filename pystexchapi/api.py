import requests
import warnings

from .request import StockExchangeTickerRequest, StockExchangePricesRequest
from .response import StockExchangeResponseParser


__all__ = ('StocksExchangeAPI',)


try:
    import cachecontrol
    cache_adapter = cachecontrol.CacheControlAdapter()
except ImportError:
    warnings.warn('Caching is not enabled. Install CacheControl for cache enabling', ImportWarning)
    cache_adapter = None


class StocksExchangeAPI(object):

    def __init__(self, ssl_enabled=True):
        super(StocksExchangeAPI, self).__init__()
        self.ssl_enabled = ssl_enabled

    def _public_request(self, req: requests.PreparedRequest) -> requests.Response:
        sess = requests.Session()

        if cache_adapter:
            sess.mount('https://', cache_adapter)
            sess.mount('http://', cache_adapter)

        response = sess.send(req, verify=self.ssl_enabled)
        response.raise_for_status()
        return response

    def ticker(self) -> dict:
        request = StockExchangeTickerRequest()
        response = StockExchangeResponseParser.parse(self._public_request(request))
        return response

    def prices(self) -> dict:
        request = StockExchangePricesRequest()
        response = StockExchangeResponseParser.parse(self._public_request(request))
        return response
