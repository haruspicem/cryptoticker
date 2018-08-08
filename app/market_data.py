import ccxt
import asyncio
import os
import ccxt.async as ccxt
import pandas as pd
import time
from datetime import datetime

async def pool_order_book(exchange, markets, interval_time):
    """Pooling order book data from exchange, in interval_time."""
    st = time.time()
    while True:
        epoch_st = time.time()
        for market in markets:
            while True:
                try:
                    order_book = await exchange.fetch_order_book(market)
                    ts = time.time()
                    yield market, order_book['bids'], order_book['asks'], ts
                    if 'BTC/USDT' in market :
                        print(exchange.describe()['name'], market, datetime.fromtimestamp(ts-st).strftime('%H:%M:%S'))
                except ccxt.errors.BaseError as e:
                    print('pool_order_book error', e)
                    continue
                break
        await asyncio.sleep(interval_time + epoch_st-time.time())

def append_to_csv(batch, path, sep=",", columns=['market', 'bids', 'asks', 'ts']):
    """Append the provided dataframe to an existing one, else writes as new."""
    df = pd.DataFrame.from_records(batch, columns=columns)
    if not os.path.isfile(path):
        df.to_csv(path, mode='a', index=False, sep=sep)
    else:
        df.to_csv(path, mode='a', index=False, sep=sep, header=False)

async def pool_exchange_data(exchange_name, currencies, batch_size=100, sleep_time=30):
    exchange = getattr(ccxt, exchange_name)()
    markets =[m for m in await exchange.load_markets() if sum(c in m for c in currencies) == 2]
    print(exchange_name, markets)
    batch = []
    async for orderbook in pool_order_book(exchange, markets, sleep_time):
        batch.append(orderbook)
        if(len(batch) > batch_size):
            append_to_csv(batch, '{}_order_book.csv'.format(exchange_name))
            batch = []

currencies = ['BTC', 'USDT', 'ETH', 'XRP', 'BCH', 'EOS', 'LTC', 'XLM', 'ADA', 'MIOTA', 'TRX', 'XMR', 'NEO', 'DASH']

asyncio.get_event_loop().run_until_complete( asyncio.gather(
     pool_exchange_data('binance', currencies),
     pool_exchange_data('bittrex', currencies),
     # pool_exchange_data('bitfinex2', currencies),
     pool_exchange_data('huobipro', currencies),
     pool_exchange_data('zb', currencies),
     #pool_exchange_data('bitmex', ['XBT', 'ADA', 'ETH', 'EOS', 'LTC', 'TRX', 'USD', 'XRP', 'BCH']),
))