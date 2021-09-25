from base import FtxClient
import ftxapi
from Stagger import Stagger
from PriceTickerRest import PriceTickerRest
from Stagger import CurrentPriceStruct

# Initialising Client
Client = FtxClient(
    api_key=ftxapi.api_key, api_secret=ftxapi.api_secret, subaccount_name=ftxapi.subaccount_name)

# Initialising Variables
crypto_pair = Client.SYMBOL_BTCUSD
crypto_amount = 0
breakeven = 0


instance_currentprice = CurrentPriceStruct()
instance_stagger = Stagger(crypto_pair=crypto_pair, Client=Client,
                           PriceStruct=instance_currentprice)
instance_priceticker = PriceTickerRest(instance_stagger, instance_currentprice)

while True:
    # locks the current variable
    instance_currentprice.current_condition.acquire()
    # unlocks the current variable and waits for currentCond.notify()
    instance_currentprice.current_condition.wait()
    print(f"Price of {crypto_pair}: ",
          instance_currentprice.current_price)
