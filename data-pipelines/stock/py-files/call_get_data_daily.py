import ccxt
from ccxt import exchanges
import time
from datetime import datetime
from zoneinfo import ZoneInfo

def request_ohlcv(exchange, pair_id):
    response = exchange.fetch_ohlcv(pair_id, timeframe='1d', limit=1)
    return response

def get_data_daily():
    exchange = ccxt.binance ({
        'rateLimit': 1,  # unified exchange property
        'headers': {
            'YOUR_CUSTOM_HTTP_HEADER': 'YOUR_CUSTOM_VALUE',
        },
        'options': {
            'adjustForTimeDifference': True,  # exchange-specific option
        }
    })

    start = time.time()
    pair_id = 'NEAR/USDT'
    tz = ZoneInfo("Asia/Ho_Chi_Minh")
    responses = request_ohlcv(exchange, pair_id)
    # print(time.time() - start)
    results = []
    for response in responses:
        response = [str(index) for index in response]
        # insert_data(response)
        response[0] = str(datetime.fromtimestamp(float(response[0])/1000, tz=tz))
        response.insert(0, pair_id)
        # print(tuple(response))
        results.append(tuple(response))
    # print(time.time() - start)
    return results