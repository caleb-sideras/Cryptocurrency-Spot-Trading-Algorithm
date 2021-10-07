from base import FtxClient
import ftxapi
import json

Client = FtxClient(
    api_key=ftxapi.api_key, api_secret=ftxapi.api_secret, subaccount_name=ftxapi.subaccount_name)

# print(Client.place_order(market="FTT/USD", side="sell",
#                          type="market", size=0.1, price=None))
# print(Client.get_fills_id("FTT/USD"))

# print(Client.place_order(market="FTT/USD", side="buy",
#       type="market", size=0.1, price=None))

all_positions = Client.get_positions()
json_balance = Client.get_balances()
fills = Client.get_fills()
# print(fills)
# print(json_balance)


def total_balance():
    total_balance = 0
    for var in json_balance:
        total_balance += var['usdValue']
        if var['usdValue'] != 0:
            print(f"{var['coin']}, {var['usdValue']}")

    print(f"Total Balance: {total_balance} \n")


def total_Pnl():
    total_realizedPnl = 0
    for var in all_positions:
        total_realizedPnl += var['realizedPnl']
        print(
            f"{var['future']}, realizedPnl: {var['realizedPnl']}, cost: {var['cost']}, entry price: {var['entryPrice']}, collateral: {var['collateralUsed']}")  # estimatedLiquidationPrice, {var['collateralUsed']}

    print(f"Total realizedPnl: {total_realizedPnl} \n")


def total_fees():
    total_fees = 0
    for var in fills:
        total_fees += var['fee']
        print(f"{var['market']}, {var['fee']}")

    print(f"Total Fees: {total_fees} \n")


total_balance()
total_Pnl()
total_fees()
