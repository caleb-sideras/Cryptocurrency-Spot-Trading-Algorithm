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
        temp_price = 0
        while True:
            try:

                temp = self.Stagger.Client.list_single_markets(
                    self.Stagger.crypto_pair)  # updated price

                # setting current variable in Price Struct to updated price
                if(temp_price != float(temp['ask'])):
                    temp_price = float(temp['ask'])
                    # locking the current variable
                    self.PriceStruct.current_condition.acquire()
                    self.PriceStruct.current_price = float(temp['ask'])
                    # notifying other conditions
                    self.PriceStruct.current_condition.notify()
                    # releasing the current variable
                    self.PriceStruct.current_condition.release()

            except Exception as e:
                print(e, "getting crypto price")

            time.sleep(self.interval)  # waiting interval

    # Every 1200 seconds, it refreshes the client
    def run2(self):
        while True:
            try:
                New_Client = FtxClient(ftxapi.api_key, ftxapi.api_secret)
                self.Stagger.Client = New_Client
                print(f"{self.Stagger.crypto_pair} refreshing client")

            except Exception as e:
                print(e, "refreshing client")

            # waiting interval
            time.sleep(1200)
