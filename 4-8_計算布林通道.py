from historical_data import get_klines_df
import pandas as pd
from talib.abstract import BBANDS

# 取得歷史資料
symbol = "BTCBUSD"
interval = "6h"
klines = get_klines_df(symbol, interval)

# 計算技術指標
data = klines.copy()
data[['upper', 'middle', 'lower']] = BBANDS(data, timeperiod=20)
