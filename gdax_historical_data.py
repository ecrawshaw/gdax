import gdax
import csv
import datetime as dt
import pandas_datareader.data as web
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
#style.use('ggplot')

#private account info
# key = ''
# b64secret = ''
# passphrase = ''
# auth_client = gdax.AuthenticatedClient(key, b64secret, passphrase)
# df_acct = pd.DataFrame(auth_client.get_accounts(), columns=['id','currency','balance','holds','available','margin_enabled','funded_amount','default_amount'])
# print(df_acct)

#gets price data
public_client = gdax.PublicClient()


start_date = dt.datetime.strptime('11Nov2017', '%d%b%Y')
timedelta = dt.timedelta(hours=1)
end_date = start_date + timedelta
timecut = '60' #in seconds

for t in range(0,100):
    start_date = start_date + timedelta
    end_date = end_date + timedelta
    print(start_date)
    print(end_date)


btc_price_data = public_client.get_product_historic_rates('BTC-USD', granularity = timecut, start = start_date.isoformat(), end = end_date)
btc = pd.DataFrame(btc_price_data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
btc = btc.set_index('time')

eth_price_data = public_client.get_product_historic_rates('ETH-USD', granularity = timecut, start = start_date.isoformat(), end = end_date)
eth = pd.DataFrame(eth_price_data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
eth = eth.set_index('time')

ltc_price_data = public_client.get_product_historic_rates('LTC-USD', granularity = timecut, start = start_date.isoformat(), end = end_date)
ltc = pd.DataFrame(ltc_price_data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
ltc = ltc.set_index('time')

#read the csv and perform operations
#df = pd.read_csv('price_info.csv', parse_dates=True, index_col=1)

def coin_df_operations(df, coin_name):
    #converts unix time to readable time based on the coin dataframe passed to it
    df['regular time'] = pd.to_datetime(df.index,unit='s')

    #converts the index to datetime so we can resample
    df.index = pd.to_datetime(df.index, unit='s')
    #print(df)

    #resamples close and volume data, the plots
    df_ohlc = df['close'].resample('24H').ohlc()
    df_volume = df['volume'].resample('24H').sum()
    df_ohlc.index = df_ohlc.index.map(mdates.date2num)
    df_ohlc.reset_index(inplace=True)
    
    #output data to .csv
    df.to_csv(coin_name + '.csv')



#loops through the list of coins
coins = [btc]#,eth,ltc]
coin_names = ['btc', 'eth', 'ltc']
for i in range(0,len(coins)):
    coins[i] = coin_df_operations(coins[i], coin_names[i])

