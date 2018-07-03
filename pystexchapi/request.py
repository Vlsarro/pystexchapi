"""
Stocks Exchange API requests
"""

from requests import PreparedRequest


__all__ = ('StockExchangeTickerRequest', 'StockExchangePricesRequest')


STOCK_EXCHANGE_BASE_URL = 'https://stocks.exchange/api2/{method}'


class StockExchangeRequest(PreparedRequest):

    def __init__(self, **kwargs):
        super(StockExchangeRequest, self).__init__()
        default_request_params = self.default_request_params()
        default_request_params.update(kwargs)
        self.prepare(**default_request_params)

    def default_request_params(self) -> dict:
        """
        Construct default parameters for request to Stocks Exchange API
        """
        _params = {
            'method': 'GET',
            'headers': {
                'Content-Type': 'application/json',
                'User-Agent': 'pystexchapi'
            }
        }
        return _params


###################################################################
# Requests for public methods
###################################################################


class StockExchangeTickerRequest(StockExchangeRequest):

    def default_request_params(self) -> dict:
        _params = super(StockExchangeTickerRequest, self).default_request_params()
        _params['url'] = STOCK_EXCHANGE_BASE_URL.format(method='ticker')
        return _params


class StockExchangePricesRequest(StockExchangeRequest):

    def default_request_params(self) -> dict:
        _params = super(StockExchangePricesRequest, self).default_request_params()
        _params['url'] = STOCK_EXCHANGE_BASE_URL.format(method='prices')
        return _params
