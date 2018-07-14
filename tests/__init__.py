import json


__all__ = ('TICKER_RESPONSE', 'PRICES_RESPONSE', 'GENERIC_ERROR_RESPONSE', 'MARKETS_RESPONSE', 'ORDERBOOK_RESPONSE',
           'GET_ACCOUT_INFO_RESPONSE', 'CURRENCIES_RESPONSE', 'MARKET_SUMMARY_RESPONSE', 'TRADE_HISTORY_RESPONSE',
           'PUBLIC_GRAFIC_RESPONSE', 'GET_ACTIVE_ORDERS_RESPONSE', 'TRADE_RESPONSE')


TICKER_RESPONSE = json.dumps([
    {
        'min_order_amount': '0.00000010',
        'ask': '0.000033',
        'bid': '0.00002905',
        'last': '0.00002905',
        'lastDayAgo': '0.00003094',
        'vol': '2665.35219464',
        'spread': '0',
        'buy_fee_percent': '0',
        'sell_fee_percent': '0',
        'market_name': 'MUN_BTC',
        'updated_time': 1520779505,
        'server_time': 1520779505
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

CURRENCIES_RESPONSE = json.dumps([
    {
        'currency': 'BTC',
        'active': True,
        'precision': 8,
        'api_precision': 8,
        'minimum_withdrawal_amount': '0.01000000',
        'minimum_deposit_amount': '0.01000000',
        'calculated_balance': '0',
        'deposit_fee_currency': 'BTC',
        'deposit_fee_const': 0,
        'deposit_fee_percent': 0,
        'withdrawal_fee_currency': 'BTC',
        'withdrawal_fee_const': 0,
        'withdrawal_fee_percent': '0.50000000',
        'currency_long': 'Bitcoin'
    },
    { 
        'currency': 'NXT',
        'active': True,
        'precision': 3,
        'api_precision': 8,
        'minimum_withdrawal_amount': '5.00000000',
        'minimum_deposit_amount': '5.00000000',
        'calculated_balance': '10',
        'deposit_fee_currency': 'NXT',
        'deposit_fee_const': '1.00000000',
        'deposit_fee_percent': 0,
        'withdrawal_fee_currency': 'NXT',
        'withdrawal_fee_const': '1.00000000',
        'withdrawal_fee_percent': 0,
        'currency_long': 'Next'
    }
])

MARKET_SUMMARY_RESPONSE = json.dumps([
    {
        'currency': 'BTC',
        'partner': 'USD',
        'currency_long': 'Bitcoin',
        'partner_long': 'USD',
        'min_order_amount': 1.000000,
        'min_buy_price': 0,
        'min_sell_price': 0,
        'buy_fee_percent': 0.002,
        'sell_fee_percent': 0.002,
        'active': False,
        'currency_precision': 8,
        'partne_precision': 3,
        'market_name': 'BTC_USD'
    }
])

TRADE_HISTORY_RESPONSE = json.dumps({
    'success': 1,
    'result': [
        {
            'id': 1234,
            'timestamp': 1523479914,
            'quantity': '2.85310747',
            'price': '0.00003251',
            'type': 'SELL'
        },
        {
            'id': 1234,
            'timestamp': 1523469243,
            'quantity': '2.85882512',
            'price': '0.00003989',
            'type': 'BUY'
        },
        {
            'id': 1234,
            'timestamp': 1523458927,
            'quantity': '0.61280000',
            'price': '0.00003250',
            'type': 'SELL'
        }
    ]
})

ORDERBOOK_RESPONSE = json.dumps({
    'success': 1,
    'result': {
        'buy': [
            {
                'Quantity': '0.00189631',
                'Rate': '58.27632628'
            },
            {
                'Quantity': '0.00325300',
                'Rate': '100.00000000'
            }
        ],
        'sell': [
            {
                'Quantity': '0.00011358',
                'Rate': '2.84740126'
            },
            {
                'Quantity': '0.00001995',
                'Rate': '0.50000000'
            }
        ]
    }
})

PUBLIC_GRAFIC_RESPONSE = json.dumps({
    'success': 1,
    'data': {
        'pair': 'STEX_BTC',
        'interval': '1D',
        'order': 'ASC',
        'since': '2018-04-11 12:30:00',
        'end': '2018-04-12 12:45:12',
        'count_pages': 1,
        'count': '100',
        'current_page': 1,
        'graf': [
            {
                'open': '0.00018027',
                'close': '0.00018027',
                'low': '0.00018027',
                'high': '0.00018027',
                'date': '2018-04-11 17:30:00'
            },
            {
                'open': '0.00021449',
                'close': '0.00021449',
                'low': '0.00021449',
                'high': '0.00021449',
                'date': '2018-04-11 21:00:00'
            }
        ]
    }
})

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

GET_ACTIVE_ORDERS_RESPONSE = json.dumps({
    'success': 1,
    'data': {
        '5303351': {
            'pair': 'BTC_NXT',
            'type': 'buy',
            'amount': '0.1',
            'rate': '5321.1',
            'is_your_order': 0,
            'timestamp': 1464352941
        },
        '5303391': {
            'pair': 'BTC_ETH',
            'type': 'buy',
            'amount': '0.3',
            'rate': '5322.2',
            'is_your_order': 0,
            'timestamp': 1464352978
        }
    }
})

TRADE_RESPONSE = json.dumps({
    'success': 1,
    'data': { 
        'funds': { 
            'UAH': '4680.84',
            'BTC': '254.7',
            'NXT': '0'
        },
        'order_id': 5616820
    }
})
