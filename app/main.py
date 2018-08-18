import sys, inspect
from app.exchanges.ExchangeBinance import ExchangeBinance

exchangesClasses = [ExchangeBinance]
exchanges = []
for item in exchangesClasses:
    exchanges.append(item())

def run(exchange):
    if (exchange.working == False):
        exchange.pull()
        return exchange

while True:
    map(run, exchanges)