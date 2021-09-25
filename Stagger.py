import threading
from base import FtxClient

# stores current price


class currentPriceStruct:
    currentCond = threading.Condition()  # current variable condition
    current = 0  # stores current price

# Stagger algo, will add later


class Stagger:
    # currentPrice = 0

    def __init__(self, breakeven=None, text=None, amount=None, cryptoid=None, timestr=None, client=None, pricestruct=None):
        self.breakeven = breakeven
        self.text = text
        self.amount = amount
        self.cryptoID = cryptoid
        self.timestr = timestr
        self.client = client
        self.priceStruct = pricestruct
