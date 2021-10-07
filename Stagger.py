from datetime import time
import threading
from base import FtxClient

# stores current price


class CurrentPriceStruct:
    current_condition = threading.Condition()  # current variable condition
    current_price = 0  # stores current price

# Stagger algo, will add later


class Stagger:
    current_price = 0
    high_price = 0
    low_price = 2147483647
    cycle = True

    def __init__(self, breakeven=None, margin=None, crypto_amount=None, crypto_pair=None, timestr=None, Client=None, PriceStruct=None, taker_fee=None):
        self.breakeven = breakeven
        self.margin = margin
        self.crypto_amount = crypto_amount
        self.crypto_pair = crypto_pair
        self.timestr = timestr
        self.Client = Client
        self.PriceStruct = PriceStruct
        self.taker_fee = taker_fee

    # initialises breakeven and current_price
    def price_init(self):
        self.update_price()
        # self.breakeven = self.current_price * (1 + self.taker_fee)
        print(f"{self.crypto_pair, self.breakeven}  price init")

    # updates current_price
    def update_price(self):
        # locks the current variable
        self.PriceStruct.current_condition.acquire()
        # unlocks the current variable and waits for current_condition.notify()
        self.PriceStruct.current_condition.wait()
        self.current_price = self.PriceStruct.current_price

    # sell cycle - checks if current_price > breakeven
    def sell_check(self):
        while self.cycle:
            self.update_price()
            if self.current_price > self.breakeven:
                self.sell_cycle()
            print(f"{self.crypto_pair} sell_check")
        return

     # buy cycle - checks if current_price < breakeven
    def buy_check(self):
        while not self.cycle:
            self.update_price()
            if self.current_price < self.breakeven:
                self.buy_cycle()
            print(f"{self.crypto_pair} buy_check")

    def sell_cycle(self):
        while self.cycle:
            self.update_price()
            if self.current_price > self.high_price:  # checks if there is a new high_price within sell cycle
                self.high_price = self.current_price
                print('1', self.crypto_pair, 'highest:',
                      self.high_price, 'breakeven:', self.breakeven)

            elif self.current_price < self.breakeven:  # checks if current_price < breakeven
                print(self.current_price,
                      'current < breakeven, returning to sell_check()')
                break

            elif self.current_price <= (1 - self.margin) * self.high_price:
                # checks if current_price <= 1 - margin% from high_price within sell cycle

                trigger_sell = self.current_price
                sell_response = self.Client.place_order(market=self.crypto_pair, side="sell",
                                                        type="market", size=self.crypto_amount, price=None)
                time.sleep(5)
                sell_fill = self.Client.get_fills_id(self.crypto_pair)[0]

                sell_fee = sell_fill['fee']
                sell_amount = sell_fill['size']
                sell_price = sell_fill['price']
                sell_total = (sell_price * sell_amount) - sell_fee

                print('SELL:'
                      '\n', sell_amount, self.crypto_pair, '=', sell_total,
                      '\n', sell_fee, 'USD fee,', 'Trigger sell:', trigger_sell)

                self.crypto_amount = sell_amount
                # self.buycorrection(sell_price)
                self.high_price = 0
                self.breakeven = sell_price * (1 - (self.taker_fee * 2))
                self.cycle = False
        return

    def buy_cycle(self):
        while not self.cycle:
            self.update_price()
            if self.current_price < self.low_price:  # checks if there is a new low_price within buy cycle
                self.low_price = self.current_price
                print('1', self.crypto_pair, 'lowest:',
                      self.low_price, 'breakeven:', self.breakeven)

            elif self.current_price > self.breakeven:  # checks if current_price > breakeven
                print(self.current_price,
                      'current < breakeven, returning to sell_check()')
                break

            elif self.current_price >= (1 + self.margin) * self.low_price:

                # checks if current_price >= 1 + margin% from high_price within buy cycle
                trigger_buy = self.current_price
                self.crypto_amount = self.current_price / self.breakeven

                sell_response = self.Client.place_order(market=self.crypto_pair, side="buy",
                                                        type="market", size=self.crypto_amount, price=None)
                time.sleep(5)
                buy_fill = self.Client.get_fills_id(self.crypto_pair)[0]

                buy_fee = buy_fill['fee']
                buy_amount = buy_fill['size']
                buy_price = buy_fill['price']
                buy_total = (buy_price * buy_amount) - buy_fee

                print('BUY:'
                      '\n', buy_amount, self.crypto_pair, '=', buy_total,
                      '\n', buy_fee, 'USD fee,', 'Trigger buy:', trigger_buy)

                self.breakeven = buy_price * (1 + self.taker_fee)
                self.crypto_amount = buy_amount
                self.low_price = 2147483647
                self.cycle = True
        return
