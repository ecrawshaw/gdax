import gdax
import csv
import time
import sys
import datetime as dt
import pandas_datareader.data as web
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates

#gets price data
public_client = gdax.PublicClient()


start_date = dt.datetime.strptime('1Dec2016', '%d%b%Y')
timedelta = dt.timedelta(days=1)
end_date = start_date + timedelta
timecut = '3600'

btc_price_data = public_client.get_product_historic_rates('BTC-USD', granularity = timecut, start = start_date.isoformat(), end = end_date.isoformat())
btc = pd.DataFrame(btc_price_data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
btc = btc.set_index('time')

eth_price_data = public_client.get_product_historic_rates('ETH-USD', granularity = timecut, start = start_date.isoformat(), end = end_date.isoformat())
eth = pd.DataFrame(eth_price_data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
eth = eth.set_index('time')

ltc_price_data = public_client.get_product_historic_rates('LTC-USD', granularity = timecut, start = start_date.isoformat(), end = end_date.isoformat())
ltc = pd.DataFrame(ltc_price_data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
ltc = ltc.set_index('time')

def coin_df_operations(df, coin_name, start_date, end_date, timedelta, timecut):
    #number of times you want to repeat your timedelta
    repeats = 365
    print('\n')
    print(coin_name)
    for t in range(0,repeats):
        sys.stdout.write('\r')
        # the exact output you're looking for:
        sys.stdout.write("%d of %s" % ((t+1),repeats))
        #sys.stdout.write('[%.2f%%]' % (100*j,1*t))
        sys.stdout.flush()

        #time operations
        start_date = start_date + timedelta
        end_date = end_date + timedelta

        time.sleep(1)
        price_data = public_client.get_product_historic_rates(coin_name + '-USD', granularity = timecut, start = start_date.isoformat(), end = end_date.isoformat())
        coin_df = pd.DataFrame(price_data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
        coin_df = coin_df.set_index('time')
        df = df.append(coin_df)

        # print(start_date)
        # print(end_date)
        # print(ltc.tail())
        # print(ltc2.tail())
    #converts unix time to readable time based on the coin dataframe passed to it
    df['regular time'] = pd.to_datetime(df.index,unit='s')

    # #converts the index to datetime so we can resample
    # df.index = pd.to_datetime(df.index, unit='s')
    # #print(df)
    #
    # #resamples close and volume data, the plots
    # df_ohlc = df['close'].resample('24H').ohlc()
    # df_volume = df['volume'].resample('24H').sum()
    # df_ohlc.index = df_ohlc.index.map(mdates.date2num)
    # df_ohlc.reset_index(inplace=True)



    df.to_csv(coin_name + '.csv')



#loops through the list of coins
coins = [btc,eth,ltc]
coin_names = ['btc', 'eth', 'ltc']
for i in range(0,len(coins)):
    coins[i] = coin_df_operations(coins[i], coin_names[i], start_date, end_date, timedelta, timecut)

#df.plot()
#plt.show()

#df['100ma'] = df['close'].rolling(window=100, min_periods=0).mean()


# df_ohlc = df['close'].resample('1H').ohlc()
# df_volume = df['volume'].resample('1H').sum()
#
# #df_ohlc.reset_index(inplace=True)
#
# #print(df_ohlc.head())
# df_ohlc.index = df_ohlc.index.map(mdates.date2num)
#
# df_ohlc.reset_index(inplace=True)
# #print(df_ohlc.values)
# #print(df_ohlc)
# #print(df_volume)
#
#
# ax1 = plt.subplot2grid((6,1),(0,0), rowspan=5, colspan=1)
# ax2 = plt.subplot2grid((6,1),(5,0), rowspan=1, colspan=1, sharex=ax1)
# ax1.xaxis_date()
#
#
# # ax1.plot(df.index, df['close'])
# # plt.show()
#
# candlestick_ohlc(ax1, df_ohlc.values, width=.01, colorup='g')
# ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
# plt.show()
#
# ax1.plot(df.index, df['close'])
# #ax1.plot(df.index, df['open'])
# ax2.bar(df.index, df['volume'])
#plt.show()

#df.plot()
#plt.show()
#print(k)
