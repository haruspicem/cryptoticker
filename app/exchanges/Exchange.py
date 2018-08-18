from app.components.OrderBook import OrderBook
import os
import app.tools as tools

class Exchange:
    # Basic class for all exchanges
    batch = []
    exchange_name = ''
    working = False

    def pull(self):
        # pull data from exchange
        self.working = True
        return 0

    def get(self, item, type, propertyName):
        # Get property from excahge response
        return ''

    def addTobatch(self, item):
        if item['data']['e'] == 'error':
            self.working = False
        else:
            steam = item['stream'].split('@')
            if (steam[1] == 'depth'):
                self.batch.append(OrderBook(
                    type=self.get(item, 'order', 'type'),
                    time=self.get(item, 'order', 'time'),
                    symbol=self.get(item, 'order', 'symbol'),
                    bids=self.get(item, 'order', 'bids'),
                    ask=self.get(item, 'order', 'ask'),
                    first_id=self.get(item, 'order', 'first_id'),
                    final_id=self.get(item, 'order', 'final_id'),
                    exchange_name=self.exchange_name,
                ))
        print("data: {}".format(item))

    def saveToCsv(self):
        # Save orderbook data to csv file
        headers = [
            'type',
            'time',
            'symbol',
            'bids',
            'ask',
            'first_id',
            'final_id',
        ]
        data = []
        for order in self.batch:
            directory = '/data/' + self.exchange_name
            if not os.path.exists(directory):
                os.makedirs(directory)
            data.append([
                order.type,
                order.time,
                order.symbol,
                order.bids,
                order.ask,
                order.first_id,
                order.final_id
            ])
        tools.append_to_csv(data, '/data/{}/order_book.csv'.format(self.exchange_name), columns=headers)