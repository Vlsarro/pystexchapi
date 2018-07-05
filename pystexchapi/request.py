"""
Stocks Exchange API requests
"""

from requests import PreparedRequest


__all__ = ('StockExchangeTickerRequest', 'StockExchangePricesRequest', 'StockExchangeRequest',
           'StockExchangeCurrenciesRequest', 'StockExchangeMarketsRequest', 'StockExchangeMarketSummaryRequest',
           'StockExchangeTradeHistoryRequest', 'StockExchangeOrderbookRequest', 'StockExchangeGraficPublicRequest')


STOCK_EXCHANGE_BASE_URL = 'https://app.stocks.exchange/api2/{method}'


class StockExchangeRequest(PreparedRequest):
    api_method = None

    def __init__(self, **kwargs):
        super(StockExchangeRequest, self).__init__()
        default_request_params = self.default_request_params()
        request_options = self.get_request_options(kwargs)
        default_request_params.update(request_options)
        self.prepare(**default_request_params)

    def get_request_options(self, kwargs: dict) -> dict:
        return {}

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


class StockExchangeCurrenciesRequest(StockExchangeRequest):
    api_method = 'currencies'


class StockExchangeMarketsRequest(StockExchangeRequest):
    api_method = 'markets'


class StockExchangeMarketSummaryRequest(StockExchangeRequest):
    api_method = 'market_summary'

    def get_request_options(self, kwargs: dict) -> dict:
        currency_1 = kwargs.pop('currency_1', None)
        currency_2 = kwargs.pop('currency_2', None)

        if not (currency_1 or currency_2):
            raise AttributeError('Invalid request parameters')
        else:
            return {
                'url': STOCK_EXCHANGE_BASE_URL.format(method=self.api_method) + '/{}/{}'.format(currency_1, currency_2)
            }


class StockExchangeTradeHistoryRequest(StockExchangeRequest):
    api_method = 'trades'

    def get_request_options(self, kwargs: dict) -> dict:
        currency_1 = kwargs.pop('currency_1', None)
        currency_2 = kwargs.pop('currency_2', None)

        if not all([currency_1, currency_2]):
            raise AttributeError('Invalid request parameters')
        else:
            return {
                'params': {'pair': '{}_{}'.format(currency_1, currency_2)}
            }


class StockExchangeOrderbookRequest(StockExchangeTradeHistoryRequest):
    api_method = 'orderbook'


class StockExchangeGraficPublicRequest(StockExchangeTradeHistoryRequest):
    api_method = 'grafic_public'

    def get_request_options(self, kwargs: dict) -> dict:
        result = super(StockExchangeGraficPublicRequest, self).get_request_options(kwargs)
        # TODO: find another way for specifying required request options
        interval = kwargs.pop('interval', None)
        order = kwargs.pop('order', None)
        count = kwargs.pop('count', None)

        if not all([interval, order, count]):
            raise AttributeError('Invalid request parameters')
        else:
            result['params'].update({
                'interval': interval,
                'order': order,
                'count': count
            })
            return result
