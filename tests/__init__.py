import json


__all__ = ('TICKER_RESPONSE', 'PRICES_RESPONSE', 'GENERIC_ERROR_RESPONSE', 'MARKETS_RESPONSE',
           'GET_ACCOUT_INFO_RESPONSE')


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
    }
])

MARKETS_RESPONSE = json.dumps([
    {
        'currency': 'PRG',
        'partner': 'BTC',
        'currency_long': 'ParagonCoin',
        'partner_long': 'Bitcoin',
        'min_order_amount': '0.00000010',
        'min_buy_price': '0.00000001',
        'min_sell_price': '0.00000001',
        'buy_fee_percent': '0.2',
        'sell_fee_percent': '0.2',
        'active': True,
        'currency_precision': 8,
        'partner_precision': 8,
        'market_name': 'PRG_BTC'
    },
    {
        'currency': 'BTC',
        'partner': 'USDT',
        'currency_long': 'Bitcoin',
        'partner_long': 'TetherUSD',
        'min_order_amount': '0.00000010',
        'min_buy_price': '0.00000001',
        'min_sell_price': '0.00000001',
        'buy_fee_percent': '0.2',
        'sell_fee_percent': '0.2',
        'active': True,
        'currency_precision': 8,
        'partner_precision': 8,
        'market_name': 'BTC_USDT'
    }
])

GENERIC_ERROR_RESPONSE = json.dumps({'success': 0, 'error': 'Invalid request'})

GET_ACCOUT_INFO_RESPONSE = json.dumps({
    'success': 1,
    'data': {
        'email': 'example@exaxmple.com',
        'username': 'example',
        'userSessions': [],
        'hash': '',
        'funds': {
            'BTK': '9832',
            'XUN': '982',
            'CHEESE': '32'
        },
        'hold_funds': {
            'BTK': '0', 'XUN': '0', 'CHEESE': '0'
        },
        'wallets_addresses': {'BTK': '', 'XUN': '', 'CHEESE': ''},
        'publick_key': {'BTK': '', 'XUN': '', 'CHEESE': ''},
        'Assets portfolio': {
            'portfolio_price': 0,
            'frozen_portfolio_price': 0,
            'count': 0,
            'assets': []
        },
        'open_orders': 0,
        'server_time': 1540885009
    }
})
