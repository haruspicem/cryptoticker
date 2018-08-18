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

    def saveToCsv(self):
        #Save orderbook data to csv file
        directory = '/data/' + self.exchange_name
        if not os.path.exists(directory):
            os.makedirs(directory)

        data = [
            self.type,
            self.time,
            self.symbol,
            self.bids,
            self.ask,
            self.first_id,
            self.final_id
        ]
        headers = [
           'type',
           'time',
           'symbol',
           'bids',
           'ask',
           'first_id',
           'final_id',
        ]
        tools.append_to_csv(data, '/data/{}/{}_order_book.csv'.format(self.exchange_name, self.symbol), ",", headers)