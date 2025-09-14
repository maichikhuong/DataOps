import ccxt
from ccxt import exchanges
import time
from datetime import datetime
from zoneinfo import ZoneInfo

def request_ohlcv_full_load(exchange, pair_id, start_date="2024-01-01T00:00:00Z"):
    since = int(exchange.parse8601(start_date))
    limit = 1000
    response = exchange.fetch_ohlcv(pair_id, timeframe="1d", since=since, limit=limit)
    return response

def get_data_full_load():
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
    responses = request_ohlcv_full_load(exchange, pair_id)
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

results = get_data_full_load()
results