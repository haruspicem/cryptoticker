import os
import app.tools as tools


class OrderBook:
    def __init__(self, type, time, symbol, bids, ask, first_id, final_id, exchange_name):
        self.type = type
        self.time = time
        self.symbol = symbol
        self.bids = bids
        self.ask = ask
        self.first_id = first_id
        self.final_id = final_id
        self.exchange_name = exchange_name