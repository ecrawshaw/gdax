import gdax
import csv
from collections import Counter
import datetime as dt
import pandas_datareader.data as web
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import numpy as np
from sklearn import svm, model_selection, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

def process_data_for_labels(coin):
    hm_hours = 7
    df = pd.read_csv('all_coins.csv')
    df.drop(['btc volume','eth volume','ltc volume'],1,inplace=True)
    df.set_index('regular time', inplace=True)
    coins = df.columns.values.tolist()
    df.fillna(0, inplace=True)

    for i in range(1, hm_hours+1):
        df['{}_{}d'.format(coin, i)] = (df[coin].shift(-i) - df[coin]) / df[coin]
    df.fillna(0, inplace=True)
    return coins, df

def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.02
    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1
    return 0

def extract_featuresets(coin):
    coins, df = process_data_for_labels(coin)

    df['{}_target'.format(coin)] = list(map(buy_sell_hold,
    df['{}_1d'.format(coin)],
    df['{}_2d'.format(coin)],
    df['{}_3d'.format(coin)],
    df['{}_4d'.format(coin)],
    df['{}_5d'.format(coin)],
    df['{}_6d'.format(coin)],
    df['{}_7d'.format(coin)],
    ))
#    print(df.head())
    vals = df['{}_target'.format(coin)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data spread:', Counter(str_vals))

    df.fillna(0, inplace=True)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

    #print(df[coin].pct_change())
    #print(coin for coin in coins)
    df_vals = df[[coin_name for coin_name in coins]].pct_change()
    #print(df_vals.head())
    # df_vals['btc'] = df_vals['btc'].pct_change()
    # df_vals['ltc'] = df_vals['ltc'].pct_change()
    # df_vals['eth'] = df_vals['eth'].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)

    X = df_vals.values
    #print(df_vals.head())
    #print(coin)

    y = df['{}_target'.format(coin)].values
    #print(df_vals.head())
    df_vals.to_csv('df_vals.csv')
    return X, y, df

def do_ml(ticker):
    X, y, df = extract_featuresets(ticker)

    #print(ticker)
    #print(df.head())
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.25)

    #clf = neighbors.KNeighborsClassifier()
    clf = VotingClassifier([('lsvc', svm.LinearSVC()),
    ('knn', neighbors.KNeighborsClassifier()),
    ('rfor', RandomForestClassifier())])
    # print(X_train)
    # print(y_train)
    # print(X_test)
    # print(y_test)
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print('Accuracy: ', confidence)
    predictions = clf.predict(X_test)
    print('Predicted spread:', Counter(predictions))

    return confidence
do_ml('btc')
#extract_featuresets('ltc')

#process_data_for_labels('btc')
