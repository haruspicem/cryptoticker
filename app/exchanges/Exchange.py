from app.components.OrderBook import OrderBook


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
        for order in self.batch:
            order.saveToCsv()