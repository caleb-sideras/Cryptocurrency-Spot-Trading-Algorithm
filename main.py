from base import FtxClient
from typing import Optional, Dict, Any, List
import caleb
from Stagger import Stagger
from PriceTickerRest import CurrentValue
from Stagger import currentPriceStruct
from requests import Request

# FTXclient
calebObj = FtxClient(
    api_key=caleb.key, api_secret=caleb.secret, subaccount_name="team_c")

currentPriceObj = currentPriceStruct()

staggerObj = Stagger(cryptoid="BTC/USD", client=calebObj,
                     pricestruct=currentPriceObj)

priceTickerObj = CurrentValue(staggerObj, currentPriceObj)

while True:
    # locks the current variable
    currentPriceObj.currentCond.acquire()
    # unlocks the current variable and waits for currentCond.notify()
    currentPriceObj.currentCond.wait()
    print("Price of BTC: ", currentPriceObj.current)
