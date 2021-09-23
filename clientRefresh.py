import config
from binance.client import Client
import pandas as pd
client = Client(config.key, config.secret)

# valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

# get timestamp of earliest date data is available
timestamp = client._get_earliest_valid_timestamp('BTCUSDT', '1d')
print(timestamp)

# request historical candle (or klines) data
# bars = client.get_historical_klines('BTCUSDT', '1d', timestamp, limit=1000)
bars = client.get_historical_klines('BTCUSDT', '1m', '1616371200000', limit=1000)
print(bars)

for line in bars:
    del line[5:]

# option 4 - create a Pandas DataFrame and export to CSV
btc_df = pd.DataFrame(bars, columns=['Date', 'Open', 'High', 'Low', 'Close'])
btc_df.set_index('Date', inplace=True)
print(btc_df.head())

btc_df.to_csv('btc_bars3.csv')