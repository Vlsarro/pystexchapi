# pystexchapi
Python client for Stocks Exchange API
## Usage

```python
from pystexchapi.api import StocksExchangeAPI

api = StocksExchangeAPI()
ticker_data = api.call('ticker')
```

For private methods you have to provide api key and api secret and then initialize api as :

```python
from pystexchapi.api import StocksExchangeAPI

api = StocksExchangeAPI(api_key='apikey', api_secret='apisecret')
account_info = api.call('get_account_info')
```
If you want add some new methods to API object or override previous ones then you have to create custom request which inherits from ```StockExchangeRequest```, example:

```python
from pystexchapi.api import StocksExchangeAPI, APIMethod
from pystexchapi.request import StockExchangeRequest
from pystexchapi.response import StockExchangeResponseParser

class MyNewRequest(StockExchangeRequest):
  api_method = 'my_request'
  
my_new_method = APIMethod(name='myrequest', request=MyNewRequest, parser=StockExchangeResponseParser)
api_methods = {my_new_method.name: my_new_method}

api = StocksExchangeAPI(api_methods=api_methods)
my_request_data = api.call('myrequest')
```
