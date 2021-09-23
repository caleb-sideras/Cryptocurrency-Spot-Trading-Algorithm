import os
import sys
import time
import config
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceWithdrawException
from staggerPrice import Stagger
from priceTicker import CurrentValue

client = Client(config.key, config.secret)

timestr = time.strftime("%Y%m%d-%H%M%S")
f = open(timestr, "x")

temp = client.get_symbol_ticker(symbol=client.SYMBOL_LINKUSD)
currentValue = float(temp['price'])
breakeven = currentValue * 1.001001
#breakeven = 1 # for testing purposes

stg = Stagger(breakeven, 0.0001, 300, client.SYMBOL_LINKUSD, timestr)
cv = CurrentValue(stg)


while True:

    while stg.sellchk():
        stg.SELL()
        time.sleep(3)

    while stg.buychk():
        stg.BUY()
        time.sleep(3)

    time.sleep(2)