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

def coin_df_operations(df, coin_name):
    #converts unix time to readable time based on the coin dataframe passed to it
    df['regular time'] = pd.to_datetime(df.index,unit='s')

    #converts the index to datetime so we can resample
    df.index = pd.to_datetime(df.index, unit='s')

    #resamples close and volume data, the plots
    df_ohlc = df['close'].resample('24H').ohlc()
    df_volume = df['volume'].resample('24H').sum()
    df_ohlc.index = df_ohlc.index.map(mdates.date2num)
    df_ohlc.reset_index(inplace=True)

    df.to_csv(coin_name)
    #sets up the upper and lower plot? not really sure
    ax1 = plt.subplot2grid((6,1),(0,0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6,1),(5,0), rowspan=1, colspan=1, sharex=ax1)
    ax1.xaxis_date()

    #creates the candlestick portions
    candlestick_ohlc(ax1, df_ohlc.values, width=.01, colorup='g')
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
    plt.show()


#loops through the list of coins
coin_names = ['btc', 'eth', 'ltc']
for i in range(0,len(coin_names)):
    #read the csv and perform operations
    csv_file = pd.read_csv(coin_names[i] + '.csv', parse_dates=True, index_col=1)
    df = pd.DataFrame(csv_file, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
    df = df.set_index('time')
    coin_df_operations(df, coin_names[i])
