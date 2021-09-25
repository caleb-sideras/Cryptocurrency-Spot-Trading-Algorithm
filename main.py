from base import FtxClient
import ftxapi
from Stagger import Stagger
from PriceTickerRest import CurrentValue
from Stagger import currentPriceStruct

# FTXclient
myObj = FtxClient(
    api_key=ftxapi.api_key, api_secret=ftxapi.api_secret, subaccount_name=ftxapi.subaccount_name)

currentPriceObj = currentPriceStruct()
staggerObj = Stagger(cryptoid="BTC/USD", client=myObj,
                     pricestruct=currentPriceObj)
priceTickerObj = CurrentValue(staggerObj, currentPriceObj)

while True:
    # locks the current variable
    currentPriceObj.currentCond.acquire()
    # unlocks the current variable and waits for currentCond.notify()
    currentPriceObj.currentCond.wait()
    print("Price of BTC: ", currentPriceObj.current)
