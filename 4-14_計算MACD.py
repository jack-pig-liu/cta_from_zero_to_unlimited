from historical_data import get_klines_df
import pandas as pd
from talib.abstract import MACD

# 取得歷史資料
symbol = "BTCBUSD"
interval = "6h"
klines = get_klines_df(symbol, interval)

# 計算技術指標
data = klines.copy()
data[['macd', 'macdsignal', 'macdhist']] = MACD(data,
                                                fastperiod=20,
                                                slowperiod=40,
                                                signalperiod=9)
