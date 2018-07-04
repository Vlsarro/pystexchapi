import json


__all__ = ('TICKER_RESPONSE', 'PRICES_RESPONSE')


TICKER_RESPONSE = json.dumps([
    {
        "min_order_amount": "0.00000010",
        "ask": "0.000033",
        "bid": "0.00002905",
        "last": "0.00002905",
        "lastDayAgo": "0.00003094",
        "vol": "2665.35219464",
        "spread": "0",
        "buy_fee_percent": "0",
        "sell_fee_percent": "0",
        "market_name": "MUN_BTC",
        "updated_time": 1520779505,
        "server_time": 1520779505
    }
])

PRICES_RESPONSE = json.dumps([
    {
        'buy': '0.00001201',
        'sell': '0.00001592',
        'market_name': 'PRG_BTC',
        'updated_time': 1530688873,
        'server_time': 1530688873
    },
    {
        'buy': '6401',
        'sell': '6471.0003',
        'market_name': 'BTC_USDT',
        'updated_time': 1530688873,
        'server_time': 1530688873
    },
    {
        'buy': '0.0000207',
        'sell': '0.00002459',
        'market_name': 'ARDOR_BTC',
        'updated_time': 1530688873,
        'server_time': 1530688873
    },
])
