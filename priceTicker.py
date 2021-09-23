import time
import threading
import config
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceWithdrawException

# client = Client(config.key, config.secret)


class CurrentValue(object):

    def __init__(self, objectstg, interval=2):
        self.interval = interval
        self.ObjectSTG = objectstg

        thread = threading.Thread(target=self.run, args=())
        thread2 = threading.Thread(target=self.run2, args=())
        thread.daemon = True
        thread2.daemon = True
        thread.start()
        thread2.start()

    def run(self):
        while True:
            # try:
            #     newclient = Client(config.key, config.secret)
            #     self.ObjectSTG.client = newclient
            #
            # except BinanceAPIException as e:
            #     print(e, "refreshing client")

            try:
                temp = self.ObjectSTG.client.get_symbol_ticker(symbol=self.ObjectSTG.productid)
                currentValue = temp['price']
                self.ObjectSTG.current = float(currentValue)

            except BinanceAPIException as e:
                print(e)

            time.sleep(self.interval)

            # currentValue = temp['price']
            # self.ObjectSTG.current = float(currentValue)

    def run2(self):
        try:
            newclient = Client(config.key, config.secret)
            self.ObjectSTG.client = newclient

        except BinanceAPIException as e:
            print(e, "refreshing client")

        time.sleep(1200)
