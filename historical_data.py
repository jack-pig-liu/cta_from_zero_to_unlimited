import os
import pandas as pd
from datetime import datetime, timezone
from binance.client import Client


def get_klines_df(symbol, interval):
    # create the Binance client, no need for api key
    client = Client("", "")

    # generate data folder
    if not os.path.exists("Data"):
        os.mkdir("Data")
    # check file exist
    file_name = f"Data//{symbol}_{interval}.csv"
    if os.path.exists(file_name):
        # read old file
        file_data = pd.read_csv(file_name)
        # file_data = file_data.astype("float")
        old_ts = file_data.iloc[-1][0]
        old_time_str = datetime.fromtimestamp(old_ts / 1000, timezone.utc).strftime(
            "%d %b %Y %H:%M:%S"
        )
        # get new data
        new_data = client.futures_historical_klines(
            symbol, interval, old_time_str)
        now_data_df = pd.DataFrame(new_data)
        now_data_df.columns = [str(i) for i in now_data_df.columns]

        # combind data
        if now_data_df.shape[0] > 0:
            dataframe_data_new = pd.concat([file_data, now_data_df], axis=0)
            dataframe_data_new = dataframe_data_new[
                ~dataframe_data_new["0"].duplicated(keep="last")
            ]
        else:
            dataframe_data_new = file_data.copy()
    else:
        # get new data
        start_str = datetime.strptime(
            "2020-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"
        ).strftime("%d %b %Y %H:%M:%S")
        tmp_data = client.futures_historical_klines(
            symbol, interval, start_str)
        dataframe_data_new = pd.DataFrame(tmp_data)
    dataframe_data_new.to_csv(file_name, index=False)
    # columns naming
    dataframe_data_new.columns = [
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume",
        "ignore",
    ]
    # set index by datetime
    dataframe_data_new["datetime"] = pd.to_datetime(
        dataframe_data_new["open_time"] * 1000000, utc=True, unit="ns"
    )
    dataframe_data_new.set_index("datetime", inplace=True)
    dataframe_data_new = dataframe_data_new.astype("float")
    return dataframe_data_new
