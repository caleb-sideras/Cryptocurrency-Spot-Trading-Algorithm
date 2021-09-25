import threading
from base import FtxClient

# stores current price


class CurrentPriceStruct:
    current_condition = threading.Condition()  # current variable condition
    current_price = 0  # stores current price

# Stagger algo, will add later


class Stagger:
    # currentPrice = 0

    def __init__(self, breakeven=None, text=None, crypto_amount=None, crypto_pair=None, timestr=None, Client=None, PriceStruct=None):
        self.breakeven = breakeven
        self.text = text
        self.crypto_amount = crypto_amount
        self.crypto_pair = crypto_pair
        self.timestr = timestr
        self.Client = Client
        self.PriceStruct = PriceStruct
