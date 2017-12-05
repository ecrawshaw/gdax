import gdax
import csv
import datetime as dt
import pandas_datareader.data as web
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates

#gets price data
public_client = gdax.PublicClient()

#
def compile_data(df, coin_name):
    #converts unix time to readable time based on the coin dataframe passed to it
    #df['regular time'] = pd.to_datetime(df.index,unit='s')
    #converts the index to datetime so we can resample
    #df.index = pd.to_datetime(df.index, unit='s')
    #coin_name = df



coin_df = pd.DataFrame()
#loops through the list of coins
coin_names = ['btc', 'eth', 'ltc']
for i in range(0,len(coin_names)):
    #read the csv and perform operations
    df = pd.read_csv(coin_names[i] + '.csv', parse_dates=True, index_col=6)
    df.drop(['time','open','high','low'],1,inplace=True)
    #df.set_index('regular time')
    df.rename(columns = {'close':coin_names[i]}, inplace=True)
    df.rename(columns = {'volume': (coin_names[i]+' volume')}, inplace=True)
    if coin_df.empty:
        coin_df = df
    else:
        coin_df = coin_df.join(df, how='outer')
    coin_df.to_csv('all_coins.csv')
    #df = pd.DataFrame(csv_file, columns=['time', 'low', 'high', 'open', 'close', 'volume', 'regular time'])
    #compile_data(df, coin_names[i])
