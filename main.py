from base import FtxClient
import ftxapi
from Stagger import Stagger
from PriceTickerRest import PriceTickerRest
from Stagger import CurrentPriceStruct

# Initialising Client
Client = FtxClient(
    api_key=ftxapi.api_key, api_secret=ftxapi.api_secret, subaccount_name=ftxapi.subaccount_name)

# Initialising Variables
taker_fee = Client.get_account_info()['takerFee']
crypto_pair = Client.SYMBOL_BTCUSD
crypto_amount = 0
breakeven = 0


instance_currentprice = CurrentPriceStruct()
instance_stagger = Stagger(crypto_pair=crypto_pair, Client=Client,
                           PriceStruct=instance_currentprice, taker_fee=taker_fee)
instance_priceticker = PriceTickerRest(instance_stagger, instance_currentprice)
instance_stagger.price_init()
while True:
    instance_stagger.buy_check()
    instance_stagger.sell_check()
