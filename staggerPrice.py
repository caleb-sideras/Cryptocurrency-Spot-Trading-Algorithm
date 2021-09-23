import math
import time

import config
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceWithdrawException

firstclient = Client(config.key, config.secret)


class Stagger:
    client = firstclient  # = Client(config.key, config.secret)
    high = 0
    low = 2147483647
    current = 0
    buyamount = 0
    cycle = True  # True = sell, False = buy

    def __init__(self, breakeven, text, amount, productid, timestr):  # TODO high and low, if no input =0,2147483647
        self.breakeven = breakeven
        self.text = text
        self.amount = amount
        self.productid = productid
        self.timestr = timestr
        self.low=1

    def sellchk(self):
        if self.current > self.breakeven and self.cycle:
            return True
        else:
            return False

    def buychk(self):
        if self.current < self.breakeven and not self.cycle:
            return True
        else:
            return False

    def SELL(self):

        if self.current > self.high:  # check if there is a new highest crypto
            self.high = self.current
            print(self.text,
                  '\n 1', self.productid, 'highest: ', self.high,
                  '\n 1', self.productid, 'break even value: ', self.breakeven)

        elif self.current < self.breakeven:
            # checking if current crypto value is less than the money spent to buy crypto
            print(self.text,
                  'current:', self.current,
                  '/ breakeven:', self.breakeven,
                  '/ highest:', self.high)

        elif self.current <= (1 - self.text) * self.high:
            # checking if current crypto has dropped value% from highest crypto value in sell cycle

            soldcurrent = self.current
            sell_fill = self.marketorder(self.client.SIDE_SELL, self.client.CRYPTO, self.amount)

            sell_fee = sell_fill[0]
            sell_amount = sell_fill[1]
            sell_amount_after_fees = sell_fill[2]
            # sell_size = sell_fill[3]
            sell_price = sell_fill[4]

            print('SELL:'
                  '\n 1', self.productid, 'value:', self.current, '/', sell_price,
                  '\n', self.amount, self.productid, 'balance (sold) for:', sell_amount, sell_amount_after_fees,
                  '\n Fees:', sell_fee, 'USDT')

            f = open(self.timestr, "a")

            f.writelines(
                '\n SELL:' +
                '\n 1 ' + str(self.productid) + ' value: ' + str(self.current) + '/' + str(sell_price) +
                '\n ' + str(self.amount) + str(self.productid) + ' balance (sold) for : ' + str(sell_amount) + str(sell_amount_after_fees) +
                '\n ' + ' Fees: ' + str(sell_fee))

            self.buyamount = math.floor(sell_amount_after_fees * 100) / 100  # round down 2 decimal places
            self.buycorrection(sell_price)
            self.high = 0
            self.cycle = False

    def BUY(self):

        if self.current < self.low:  # check if there is a new highest crypto
            self.low = self.current
            print(self.text,
                  '\n 1', self.productid, 'lowest: ', self.low,
                  '\n 1', self.productid, 'break even value: ', self.breakeven)

        elif self.current > self.breakeven:
            # checking if current crypto value is more than the money spent to sell crypto
            print(self.text,
                  'current:', self.current,
                  '/ breakeven:', self.breakeven,
                  '/ lowest:', self.low)

        elif self.current >= (1 + self.text) * self.low:
            # checking if current crypto has risen text% from lowest crypto value in buy cycle

            boughtcurrent = self.current
            buy_fill = self.marketorder(self.client.SIDE_BUY, self.client.USD, self.buyamount)

            buy_fee = buy_fill[0]
            buy_price = buy_fill[4]
            buy_size = buy_fill[3]
            actual_buyamount = buy_fill[2]


            print('BUY:'
                  '\n 1', self.productid, 'value:', boughtcurrent, '/', buy_price,
                  '\n', self.buyamount, '/', actual_buyamount, 'USD (bought):', buy_size,
                  '\n Fees:', buy_fee, ' USDT')

            f = open(self.timestr, "a")

            f.writelines(
                '\n BUY:' +
                '\n 1 ' + str(self.productid) + ' value: ' + str(boughtcurrent) + '/' + str(buy_price) +
                '\n ' + str(self.buyamount) + '/' + str(actual_buyamount) + ' USD (bought): ' + str(buy_size) +  # TODO self.buyamount not the actual amount, eg 13 = 12.9805
                '\n Fees: ' + str(buy_fee))

            self.amount = buy_size
            self.sellcorrection(buy_price)
            self.low = 2147483647
            self.cycle = True

    def sellcorrection(self, buyprice):
        increment = 1.001001  # increment (1.001 * 0.001)
        self.breakeven = buyprice * increment

    def buycorrection(self, sellprice):
        decrement = 0.998  # 0.1 * 2
        self.breakeven = sellprice * decrement

    def marketorder(self, side, orderType, amount):

        if orderType == 'USD':
            try:
                r = self.client.create_order(
                    symbol=self.productid,
                    side=side,
                    type=self.client.ORDER_TYPE_MARKET,
                    quoteOrderQty=amount
                )
            except BinanceAPIException as e:
                print(e)
        else:
            try:
                r = self.client.create_order(
                    symbol=self.productid,
                    side=side,
                    type=self.client.ORDER_TYPE_MARKET,
                    quantity=amount
                )
            except BinanceAPIException as e:
                print(e)

        time.sleep(5)
        info = self.fillinfo(r)
        return info

    # def scalefactor(self, amount, bool):
    #     if bool:
    #         return amount * 100000000
    #     else:
    #         return amount / 100000000

    def fillinfo(self, r):
        totalUSDTcommission = 0
        cumprice = 0
        data = [1, 2, 3, 4, 5]
        fills = r['fills']
        x = len(fills)  # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#new-order--trade
        for i in range(0, x):
            USDTcommission = float(fills[i]['commission'])
            totalUSDTcommission += USDTcommission

        for i in range(0, x):
            price = float(fills[i]['price'])
            cumprice += price

        avgprice = cumprice / x

        USDTsold = float(r['cummulativeQuoteQty'])
        USDTsoldactual = USDTsold - totalUSDTcommission
        orderID = float(r['orderId'])
        size = float(r['executedQty'])

        data[0] = totalUSDTcommission
        data[1] = USDTsold
        data[2] = USDTsoldactual
        data[3] = size
        data[4] = avgprice
        return data

    # def round_decimals_down(number: float, decimals: int = 2):
    #     """
    #     Returns a value rounded down to a specific number of decimal places.
    #     """
    #     if not isinstance(decimals, int):
    #         raise TypeError("decimal places must be an integer")
    #     elif decimals < 0:
    #         raise ValueError("decimal places has to be 0 or more")
    #     elif decimals == 0:
    #         return math.floor(number)
    #
    #     factor = 10 ** decimals
    #     return math.floor(number * factor) / factor
