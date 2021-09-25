from base import FtxClient
from typing import Optional, Dict, Any, List
import personal_details
from Stagger import Stagger
from PriceTickerRest import CurrentValue
from Stagger import currentPriceStruct
from requests import Request

# FTXclient
myObj = FtxClient(
    api_key=personal_details.api_key, api_secret=personal_details.api_secret, subaccount_name=personal_details.subaccount_name)

currentPriceObj = currentPriceStruct()
staggerObj = Stagger(cryptoid="BTC/USD", client=myObj, pricestruct=currentPriceObj)
priceTickerObj = CurrentValue(staggerObj, currentPriceObj)

while True:
    # locks the current variable
    currentPriceObj.currentCond.acquire()
    # unlocks the current variable and waits for currentCond.notify()
    currentPriceObj.currentCond.wait()
    print("Price of BTC: ", currentPriceObj.current)
