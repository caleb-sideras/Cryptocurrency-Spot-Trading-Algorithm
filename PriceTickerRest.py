import time
import threading
import ftxapi
from base import FtxClient

# Explainerman for artem grislis!!!
class CurrentValue(object):

    def __init__(self, stagger=None, pricestruct=None, interval=2, ):
        self.Stagger = stagger  # Stagger Object passed in
        self.priceStruct = pricestruct  # Price Struct Object passed in
        self.interval = interval  # time interval

        # creates two threads and allocates a function to each thread
        thread = threading.Thread(target=self.run, args=())
        thread2 = threading.Thread(target=self.run2, args=())
        thread.daemon = True
        thread2.daemon = True
        thread.start()
        thread2.start()

    # This thread gets the price of a cryptoID every interval
    def run(self):
        while True:
            try:

                temp = self.Stagger.client.list_single_markets(
                    self.Stagger.cryptoID)  # updated price
                self.priceStruct.currentCond.acquire()  # locking the current variable
                # setting current variable in Price Struct to updated price
                self.priceStruct.current = float(temp['ask'])
                self.priceStruct.currentCond.notify()  # notifying other conditions
                self.priceStruct.currentCond.release()  # releasing the current variable

            except Exception as e:
                print(e, "getting crypto price")

            time.sleep(self.interval)  # waiting interval

    # Every 1200 seconds, it refreshes the client
    def run2(self):
        while True:
            try:
                newclient = FtxClient(ftxapi.py.key, ftxapi.py.secret)
                self.Stagger.client = newclient

            except Exception as e:
                print(e, "refreshing client")

            # waiting interval
            time.sleep(1200)
