"""
Stocks Exchange API requests
"""

from requests import PreparedRequest


__all__ = ('StockExchangeTickerRequest', 'StockExchangePricesRequest', 'StockExchangeRequest')


STOCK_EXCHANGE_BASE_URL = 'https://stocks.exchange/api2/{method}'


class StockExchangeRequest(PreparedRequest):
    api_method = None

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
            },
            'url': STOCK_EXCHANGE_BASE_URL.format(method=self.api_method)
        }
        return _params


###################################################################
# Requests for public methods
###################################################################


class StockExchangeTickerRequest(StockExchangeRequest):
    api_method = 'ticker'


class StockExchangePricesRequest(StockExchangeRequest):
    api_method = 'prices'
