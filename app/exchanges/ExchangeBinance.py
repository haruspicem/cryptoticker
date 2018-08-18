import itertools
import asyncio
import time
import app.tools as tools
from app.exchanges.Exchange import Exchange
from binance.client import Client
from binance.websockets import BinanceSocketManager


class ExchangeBinance(Exchange):
    exchange_name = 'binance'

    def pull(self):
        config = tools.getConfig('binance')
        config_global = tools.getConfig('global')
        if (config):
            client = Client(config['public_key'], config['secret_key'])
            couples = itertools.combinations(config_global['currencies'], 2)
            bm = BinanceSocketManager(client)
            sockets = []
            for couple in couples:
                sockets.append('{}@depth'.format(''.join(couple).lower()))
                # sockets.append('{}@trade'.format(''.join(couple).lower()))
            bm.start_multiplex_socket(sockets, self.addTobatch)
            bm.start()
            self.working = True
            for orderbook in self.batch:
                orderbook.saveToCsv()
                # time.sleep(30)
                # await asyncio.sleep(30)

    def get(self, item, type, propertyName):
        map = {
            'order': {
                'type': item['data']['e'],
                'time': item['data']['E'],
                'symbol': item['data']['s'],
                'first_id': item['data']['U'],
                'final_id': item['data']['u']
            }
        }
        if (propertyName != 'bids' and propertyName != 'ask'):
            result = map[type][propertyName]
        else:
            name = 'a'
            result = []
            if (propertyName == 'bids' ):
                name = 'b'
            for item in item['data'][name]:
                result.append({
                    'price': item[0],
                    'quantity': item[1],
                })
        return result




test = ExchangeBinance()
test.pull()