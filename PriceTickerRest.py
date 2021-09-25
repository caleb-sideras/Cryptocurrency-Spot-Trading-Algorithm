import time
import threading
import ftxapi
from base import FtxClient

# Explainerman for artem grislis!!!


class PriceTickerRest(object):

    def __init__(self, Stagger=None, PriceStruct=None, interval=2, ):
        self.Stagger = Stagger  # Stagger Object passed in
        self.PriceStruct = PriceStruct  # Price Struct Object passed in
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

                temp = self.Stagger.Client.list_single_markets(
                    self.Stagger.crypto_pair)  # updated price
                self.PriceStruct.current_condition.acquire()  # locking the current variable
                # setting current variable in Price Struct to updated price
                self.PriceStruct.current_price = float(temp['ask'])
                self.PriceStruct.current_condition.notify()  # notifying other conditions
                self.PriceStruct.current_condition.release()  # releasing the current variable

            except Exception as e:
                print(e, "getting crypto price")

            time.sleep(self.interval)  # waiting interval

    # Every 1200 seconds, it refreshes the client
    def run2(self):
        while True:
            try:
                New_Client = FtxClient(ftxapi.api_key, ftxapi.api_secret)
                self.Stagger.Client = New_Client

            except Exception as e:
                print(e, "refreshing client")

            # waiting interval
            time.sleep(1200)
