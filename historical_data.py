import os
import pandas as pd
from datetime import datetime
from binance.client import Client


def get_klines_df(symbol, interval):
    # create the Binance client, no need for api key
    client = Client("", "")

    # generate data folder
    if not os.path.exists('Data'):
        os.mkdir('Data')

    # check file exist
    file_name = 'Data//%s.csv' % (symbol)
    if os.path.exists(file_name):
        # read old file
        file_data = pd.read_csv(file_name)
        old_ts = file_data.iloc[-1][0]
        old_time_str = datetime.fromtimestamp(old_ts / 1000).strftime("%d %b %Y %H:%M:%S")
        # get new data
        tmp_data = client.futures_historical_klines(symbol, interval, old_time_str)
        dataframe_data = pd.DataFrame(tmp_data)
        # combind data
        if dataframe_data.shape[0] > 0:
            dataframe_data_new = pd.concat(file_data, dataframe_data)
            dataframe_data_new = dataframe_data_new[~dataframe_data_new[0].duplicated(keep='last')]
        else:
            dataframe_data_new = file_data.copy()
    else:
        # get new data
        start_str = datetime.strptime('2020-01-01 00:00:00', '%Y-%m-%d %H:%M:%S').strftime("%d %b %Y %H:%M:%S")
        tmp_data = client.futures_historical_klines(symbol, interval, start_str)
        dataframe_data_new = pd.DataFrame(tmp_data)

    dataframe_data_new.to_csv(file_name, index=False)
    # columns naming
    dataframe_data_new.columns = ['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time',
                                  'Quote_asset_volume', 'Number_of_trades', 'Taker_buy_base_asset_volume',
                                  'Taker_buy_quote_asset_volume', 'Ignore']
    # set index by datetime
    dataframe_data_new['datetime'] = pd.to_datetime(dataframe_data_new['Open_time'] * 1000000, unit='ns')
    dataframe_data_new.set_index('datetime', inplace=True)

    return dataframe_data_new
