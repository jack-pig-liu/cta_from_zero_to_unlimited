from historical_data import get_klines_df
from binance.client import Client
from talib.abstract import SMA
import pandas as pd
import time

# 取得歷史資料
symbol = "BTCBUSD"
interval = "15m"
klines = get_klines_df(symbol, interval)

# 計算指標以及定義策略(迴圈寫法)
start_ts = time.time()
data = klines.copy()

for index, row in data.iterrows():
    if row['low'] == row['open']:
        data.loc[index, 'up'] = True
    else:
        data.loc[index, 'up'] = False

print(f"迴圈寫法共花費:{time.time() - start_ts}秒")

# 計算指標以及定義策略(向量化寫法)
start_ts = time.time()
data = klines.copy()

data['up'] = False
data.loc[data["low"] > data["open"], "up"] = True
print(f"向量化寫法共花費:{time.time() - start_ts}秒")
